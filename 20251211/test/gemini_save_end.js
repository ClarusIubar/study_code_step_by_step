(function main() {
    
    // =================================================================
    // 0. [사용자 설정 영역] 출력 전략만 선택하세요!
    // =================================================================
    
    // 1. 출력 전략: 'CLIPBOARD' (가장 안정적인 단일 복사) 또는 'SPLIT_FILES' (턴별 파일 분할)
    const OUTPUT_STRATEGY = 'CLIPBOARD';
    // NOTE: 포맷은 옵시디언(OBSIDIAN) 콜아웃으로 고정됩니다.
    const OUTPUT_FORMATTER = 'OBSIDIAN';
    const CLIPBOARD_STRATEGY = 'SINGLE'; 
    
    
    // =================================================================
    // 0. [내부 설정] 내부 사용 상수 및 스타일
    // =================================================================
    
    const INTERNAL_CONSTANTS = {
        OUTPUT_STRATEGY: OUTPUT_STRATEGY, 
        OUTPUT_FORMATTER: OUTPUT_FORMATTER,
        CLIPBOARD_STRATEGY: CLIPBOARD_STRATEGY, 
        
        // UI/메시지 관련
        PANEL_ID: "gemini-export-panel",
        STATUS_INITIAL: "🕵️ 스크롤을 살짝 올려 대화 내용을 모두 로드해주세요.",
        STATUS_LOADING: "🤖 로딩 중... (Human Mode)",
        STATUS_WAITING: (delay) => `⏳ 로딩 중... (${(delay / 1000).toFixed(1)}s)`,
        STATUS_START: "⬇️ 데이터 수집 및 마크다운 준비 중...", 
        STATUS_FORMATTING: "🧹 콜아웃 포맷팅 및 클립보드 복사 준비 중...", 
        STATUS_DOWNLOAD: "💾 파일 분할 완료. 다운로드 시작!", 
        STATUS_SUCCESS: "✅ 완료!", 
        
        CLOSE_TEXT: "닫기 X",
        ALERT_SUCCESS_COPY: (total) => `✅ 복사 완료! (${total}개 대화 쌍)\n\n클립보드에 복사되었습니다. 옵시디언에 붙여넣으세요.`,
        ALERT_SUCCESS_SPLIT: (total) => `✅ ${total}개의 대화 턴 파일이 생성되어 다운로드되었습니다.`,
        ALERT_FAIL: "복사 실패",
        
        COUNT_LABEL_FMT: (len) => `수집된 대화 쌍: ${len}`,
        
        // 파싱 및 필터링
        CLEANUP_TEXT: [/Show drafts/g, /View other drafts/g],
        FILTER_LIST: ['button', 'svg', 'mat-icon', 'style', 'script', 'noscript', 'g', 'path'],
        FILTER_CLASSES: ['trash-icon', 'input-area', 'capabilities_disclaimer'],
        FILTER_ATTRIBUTES: { 'role': 'button' },
        
        // 포맷팅 관련 (옵시디언 전용)
        CALLOUT_USER: "question",
        CALLOUT_MODEL: "tip",
        CALLOUT_INFO: "info"
    };

    const STYLES = {
        COLOR_INITIAL: "#fbc02d", 
        COLOR_LOADING: "#42a5f5", 
        COLOR_SUCCESS: "#69f0ae", 
        PANEL: { 
            position: "fixed", top: "20px", right: "20px", width: "320px",
            background: "rgba(20, 20, 20, 0.95)", color: "#fff", borderRadius: "12px",
            padding: "20px", zIndex: "999999", border: "1px solid #555",
            boxShadow: "0 10px 40px rgba(0,0,0,0.8)", fontFamily: "sans-serif",
            display: "flex", flexDirection: "column", gap: "10px"
        },
        STATUS: { fontWeight: "bold", fontSize: "15px", textAlign: "center" },
        COUNT: { textAlign: "right", fontSize: "12px", color: "#aaa" },
        COPY_BUTTON: {
            padding: "12px", background: "#7b1fa2", color: "white", border: "none",
            borderRadius: "6px", cursor: "pointer", fontWeight: "bold", marginTop: "10px", fontSize: "14px"
        },
        CLOSE_BUTTON: {
            background: "transparent", border: "none", color: "#777", cursor: "pointer", alignSelf: "flex-end", fontSize: "12px"
        }
    };
    
    const CONSTANTS = INTERNAL_CONSTANTS; 

    let STATE_MANAGER = {
        lockedScrollTarget: null,
        autoTimer: null,
        countInterval: null,
        statusTextEl: null,
        countLabelEl: null
    };

    let state = STATE_MANAGER;


    // =================================================================
    // 1. [정책 제어 및 포맷터 정의]
    // =================================================================
    
    /** 정책 가드레일: 옵시디언 단일 전략으로 고정 */
    function applyPolicyGuardrail() {
        return CONSTANTS.OUTPUT_STRATEGY;
    }
    
    // --- 1.2. 포맷터 함수 정의 ---
    
    /** 옵시디언 콜아웃 포맷 (유일한 포맷터) */
    function formatToObsidianCallout(turnType, text) {
        const calloutType = turnType === 'User' ? CONSTANTS.CALLOUT_USER : CONSTANTS.CALLOUT_MODEL;
        const quotedText = text.split('\n').map(line => `> ${line}`).join('\n');
        return `> [!${calloutType}] ${turnType}\n${quotedText}\n\n`;
    }
    
    const FORMATTER_MAP = {
        'OBSIDIAN': formatToObsidianCallout,
    };

    
    // =================================================================
    // 2. [DOM 파서] 순수 함수: DOM 노드를 표준 마크다운으로 변환합니다.
    // =================================================================
    
    function parseDomToMarkdown(node) {
        if (node.nodeType === Node.TEXT_NODE) return node.textContent;
        if (node.nodeType !== Node.ELEMENT_NODE) return "";

        const tag = node.tagName.toLowerCase();
        
        if (CONSTANTS.FILTER_LIST.includes(tag) || 
            CONSTANTS.FILTER_CLASSES.some(cls => node.classList.contains(cls)) || 
            Object.entries(CONSTANTS.FILTER_ATTRIBUTES).some(([attr, val]) => node.getAttribute(attr) === val)) { 
            return "";
        }

        if (tag === 'pre') {
            const codeEl = node.querySelector('code') || node;
            const text = codeEl.textContent;
            const langMatch = (codeEl.className + " " + node.className).match(/language-([a-zA-Z0-9_-]+)/);
            const lang = langMatch ? langMatch[1] : '';
            return `\n\`\`\`${lang}\n${text}\n\`\`\`\n`;
        }
        if (tag === 'code') return `\`${node.textContent}\``;

        let childrenMd = "";
        node.childNodes.forEach(child => {
            childrenMd += parseDomToMarkdown(child);
        });

        switch (tag) {
            case 'p': return `\n${childrenMd.trim()}\n\n`;
            case 'br': return `\n`;
            case 'b': case 'strong': return `**${childrenMd}**`;
            case 'i': case 'em': return `*${childrenMd}*`;
            case 'li': return `- ${childrenMd.trim()}\n`;
            case 'ul': case 'ol': return `\n${childrenMd}\n`;
            case 'a': return `[${childrenMd}](${node.getAttribute('href') || '#'})`;
            case 'h1': case 'h2': case 'h3': case 'h4': return `\n**${childrenMd.trim()}**\n`;
            case 'table': return `\n${childrenMd}\n`;
            case 'tr': return `| ${childrenMd} |\n`;
            case 'td': case 'th': return `${childrenMd} | `;
            default: return childrenMd;
        }
    }
    
    // =================================================================
    // 3. [코어 로직] 순수 함수: 턴을 결합하여 처리합니다.
    // =================================================================
    
    /** 텍스트 정제만 수행하는 헬퍼 함수 */
    function cleanText(text) {
        CONSTANTS.CLEANUP_TEXT.forEach(regex => {
            text = text.replace(regex, '');
        });
        return text.replace(/\n{3,}/g, '\n\n').trim();
    }
    
    /** 메타데이터 (제목, URL 등)를 포맷하는 함수 */
    function getFormattedMetadata(title, url) {
        const today = new Date().toISOString().split('T')[0];
        const metadataText = `- **Date**: ${today}\n- **Source**: [Link](${url})`;
        
        // 옵시디언 포맷만 지원
        const formatterFn = FORMATTER_MAP[CONSTANTS.OUTPUT_FORMATTER];
        return `# ${title}\n\n` + formatterFn('Metadata', metadataText);
    }
    
    /**
     * 순수 함수: 전체 대화 턴 배열을 포맷팅하여 최종 마크다운을 생성합니다. (CLIPBOARD 전용)
     */
    async function generateFormattedMarkdown(turns, title) {
        let md = "";
        
        const formatterFn = FORMATTER_MAP[CONSTANTS.OUTPUT_FORMATTER];
        
        // --- 3.1. 메타데이터 처리 (SINGLE 방식만 남음) ---
        md += getFormattedMetadata(title, window.location.href);

        // --- 3.2. 대화 턴 처리 (사용자-제미나이 쌍으로 묶음) ---
        const userTurns = turns.filter(t => t.tagName.toLowerCase() === 'user-query');
        const totalTurns = userTurns.length;

        for (let i = 0; i < totalTurns; i++) {
            const userTurn = userTurns[i];
            const modelTurn = userTurn.nextElementSibling; 

            let userText = cleanText(parseDomToMarkdown(userTurn));
            let modelText = (modelTurn && modelTurn.tagName.toLowerCase() === 'model-response') 
                          ? cleanText(parseDomToMarkdown(modelTurn)) : "";
            
            // 옵시디언 단일 복사: 콜아웃으로 순차 배치
            md += formatterFn('User', userText);
            md += formatterFn('Gemini', modelText);
            
            if (i % 5 === 0) await new Promise(r => setTimeout(r, 0));
        }
        return { markdown: md, total: totalTurns };
    }
    
    /**
     * 브라우저의 다운로드 기능을 이용해 텍스트를 파일로 저장합니다. (SPLIT_FILES 전용)
     */
    function downloadFile(filename, text) {
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }

    /**
     * 대화 턴별로 파일을 분할하여 다운로드합니다. (SPLIT_FILES 전용)
     */
    async function generateAndDownloadSplitFiles(turns, title) {
        const userTurns = turns.filter(t => t.tagName.toLowerCase() === 'user-query');
        const total = userTurns.length;
        const baseTitle = title.replace(/[^a-zA-Z0-9\sㄱ-ㅎㅏ-ㅣ가-힣]/g, '_').substring(0, 30).trim() || 'Gemini_Chat';
        
        const formatterFn = FORMATTER_MAP[CONSTANTS.OUTPUT_FORMATTER];
        
        for (let i = 0; i < total; i++) {
            const userTurn = userTurns[i];
            const modelTurn = userTurn.nextElementSibling; 

            let userText = cleanText(parseDomToMarkdown(userTurn));
            let modelText = (modelTurn && modelTurn.tagName.toLowerCase() === 'model-response') 
                          ? cleanText(parseDomToMarkdown(modelTurn)) : "";
            
            // 옵시디언 포맷 적용
            let md = getFormattedMetadata(title, window.location.href);
            md += formatterFn('User', userText);
            md += formatterFn('Gemini', modelText);

            const indexStr = String(i + 1).padStart(3, '0');
            const filename = `${baseTitle}_Turn_${indexStr}.md`;
            
            downloadFile(filename, md);

            await new Promise(r => setTimeout(r, 100)); 
        }
        return total;
    }

    // =================================================================
    // 4. [I/O 및 UI] 사이드 이펙트 관리 영역
    // =================================================================
    
    function createUIElement(tag, styles = {}, text = "") {
        const el = document.createElement(tag);
        Object.assign(el.style, styles);
        if (text) el.innerText = text;
        return el;
    }

    function setupUIPanel() {
        const oldPanel = document.getElementById(CONSTANTS.PANEL_ID);
        if (oldPanel) oldPanel.remove();

        const panel = createUIElement("div", STYLES.PANEL);
        panel.id = CONSTANTS.PANEL_ID;

        const statusText = createUIElement("div", { ...STYLES.STATUS, color: STYLES.COLOR_INITIAL }, CONSTANTS.STATUS_INITIAL);
        const countLabel = createUIElement("div", STYLES.COUNT, CONSTANTS.COUNT_LABEL_FMT(0));
        
        let btnText = CONSTANTS.OUTPUT_STRATEGY === 'CLIPBOARD' ? '📥 옵시디언 마크다운 복사' : '💾 옵시디언 파일 분할 다운로드';
        
        const copyBtn = createUIElement("button", STYLES.COPY_BUTTON, btnText); 
        const closeBtn = createUIElement("button", STYLES.CLOSE_BUTTON, CONSTANTS.CLOSE_TEXT);
        
        state.statusTextEl = statusText;
        state.countLabelEl = countLabel;

        closeBtn.onclick = cleanupResources;
        copyBtn.onclick = handleExecution; 

        panel.appendChild(statusText);
        panel.appendChild(countLabel);
        panel.appendChild(copyBtn);
        panel.appendChild(closeBtn);
        document.body.appendChild(panel);
    }
    
    function updateTurnCount() {
        const len = document.querySelectorAll('user-query').length; 
        state.countLabelEl.innerText = CONSTANTS.COUNT_LABEL_FMT(len);
    }

    function startScrollSimulation() {
        const baseInterval = 800; 
        function loop() {
            if (!state.lockedScrollTarget) return;
            const randomDelay = Math.floor(Math.random() * 500) + baseInterval;
            state.lockedScrollTarget.scrollTo({ top: 0, behavior: 'smooth' });
            state.statusTextEl.innerText = CONSTANTS.STATUS_WAITING(randomDelay);
            state.autoTimer = setTimeout(loop, randomDelay);
        }
        loop();
    }

    function handleScrollDetection(e) {
        if (state.lockedScrollTarget) return;
        const target = e.target;
        const scroller = target === document ? document.scrollingElement : target;
        
        if (scroller && scroller.scrollHeight > scroller.clientHeight) {
            state.lockedScrollTarget = scroller;
            state.statusTextEl.innerText = CONSTANTS.STATUS_LOADING;
            state.statusTextEl.style.color = STYLES.COLOR_LOADING;
            
            startScrollSimulation();
            state.countInterval = setInterval(updateTurnCount, 800);
        }
    }

    /** 스크롤 권한 잠금을 확실히 해제하는 핵심 정리 함수. */
    function cleanupResources() {
        window.removeEventListener('scroll', handleScrollDetection, { capture: true });
        if (state.autoTimer) clearTimeout(state.autoTimer);
        if (state.countInterval) clearInterval(state.countInterval);
        
        state.lockedScrollTarget = null; 
        
        const panel = document.getElementById(CONSTANTS.PANEL_ID);
        if (panel) panel.remove();
    }
    

    /** 메인 실행 로직: 옵시디언 전략에 따라 실행 */
    async function handleExecution() {
        // 0. 스크롤 잠금 및 타이머를 즉시 해제합니다.
        cleanupResources();

        state.statusTextEl.innerText = CONSTANTS.STATUS_START;
        
        // 1. 정책 가드레일 적용 및 최종 전략 결정
        const finalStrategy = applyPolicyGuardrail();
        
        // 2. 턴 로딩 유도 및 대기
        const scrollTarget = document.scrollingElement;
        if (scrollTarget) scrollTarget.scrollTo({ top: scrollTarget.scrollHeight, behavior: 'smooth' });
        await new Promise(r => setTimeout(r, 1000));

        // 3. 데이터 수집
        const turns = Array.from(document.querySelectorAll('user-query, model-response'));
        if (turns.length === 0) {
            state.statusTextEl.innerText = "❌ 대화 턴을 찾을 수 없습니다.";
            return;
        }
        
        const title = document.title.replace('Gemini - ', '') || "Gemini Chat";
        
        // 4. 최종 전략 실행
        if (finalStrategy === 'CLIPBOARD') {
            state.statusTextEl.innerText = CONSTANTS.STATUS_FORMATTING;
            
            // 클립보드 복사
            const result = await generateFormattedMarkdown(turns, title); 
            const md = result.markdown;
            const total = result.total;
            
            const ta = document.createElement('textarea');
            ta.value = md;
            document.body.appendChild(ta);
            ta.select();
            
            try {
                document.execCommand('copy');
                state.statusTextEl.innerText = CONSTANTS.STATUS_SUCCESS;
                state.statusTextEl.style.color = STYLES.COLOR_SUCCESS;
                alert(CONSTANTS.ALERT_SUCCESS_COPY(total));
                cleanupResources();
            } catch (e) { 
                alert(CONSTANTS.ALERT_FAIL); 
            }
            document.body.removeChild(ta);

        } else if (finalStrategy === 'SPLIT_FILES') {
            // 파일 분할 다운로드
            try {
                state.statusTextEl.innerText = CONSTANTS.STATUS_DOWNLOAD;
                const total = await generateAndDownloadSplitFiles(turns, title);
                
                state.statusTextEl.innerText = CONSTANTS.STATUS_SUCCESS;
                state.statusTextEl.style.color = STYLES.COLOR_SUCCESS;
                alert(CONSTANTS.ALERT_SUCCESS_SPLIT(total));
                cleanupResources();
            } catch (e) {
                console.error("File Generation Error:", e);
                state.statusTextEl.innerText = "🚨 파일 생성 및 다운로드 중 알 수 없는 오류 발생.";
            }
        }
    }
    
    // 전체 스크립트 실행 시작 (I/O Side Effect)
    setupUIPanel();
    window.addEventListener('scroll', handleScrollDetection, { capture: true, once: false });
    
})();
# ( )는 ( )을 깜빡하고 놓고와서 ( )다.

# def sentence_generator(name, object, result):
#     print(f"{name}는 {object}을 깜빡 놓고와서 {result}다.")

# sentence_generator("효현이", "안경", "앞이 안보인")

# (요즘)은 (독감시즌)이라 (면역력)이 중요합니다. 그러니까 (따뜻한 물)을 많이 (마시)세요.
# time, season, important_target, object, action

def make_html(title, contents): # 주어/목적어
    result = f"""
<html>
    <head><title>
    {title}
    </title></head>
    <body> 
    {contents} 
    </body>
</html>
"""
    print(result)

make_html("안녕하세요", "당신은 지금 다크웹에 들어오셨습니다.")
import requests
from chaojiying import Chaojiying_Client
import lxml.etree
page_url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
user_url = 'https://so.gushiwen.cn/user/collect.aspx'
session  =requests.session()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}
def get_img():
    res = requests.get(url=page_url,headers=headers)
    soul = lxml.etree.HTML(res.text)
    item = soul.xpath('//*[@id="imgCode"]/@src')[0]
    item1 = soul.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
    item2 = soul.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
    print(item1,item2)
    link = 'https://so.gushiwen.cn/'+item
    response = session.get(link, headers=headers)
    text = response.content
    print('正在下载验证码图片')
    with open('code.png', 'wb')as f:
        f.write(text)
    return item1,item2
def get_code():
    print('解码ing')
    chaojiying = Chaojiying_Client('username', 'userpasd', 'key')
    # username超级鹰的用户名
    # userpasd密码
    # key独有的key
    im = open('code.png', 'rb').read()
    code = chaojiying.PostPic(im, 1004)["pic_str"]
    print(code)
    return code
def login(username,password):
    data = get_img()
    data1 = data[0]
    data2 = data[1]
    code = get_code()
    print("data1",data1)
    print("data2", data2)
    print("code", code)
    data = {
        "__VIEWSTATE":data1,
        "__VIEWSTATEGENERATOR":data2,
        "from": "http://so.gushiwen.cn/user/collect.aspx",
        "email": username,
        "pwd": password,
        "code": code,
        "denglu": "登录",
    }
    res = session.post(page_url,headers=headers,data=data)
    print("登陆ing")
    print("res",res)
    response = session.get(user_url,headers=headers)
    # 借助cookies登录个人主页
    print("response",response)
    print(response.text)

if __name__ == '__main__':
    username = input('imput your username')
    password = input('imput your password')
    login(username,password)
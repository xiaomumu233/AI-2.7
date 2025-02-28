# -*- coding: utf-8 -*-
import math
import os
import subprocess
import sys
import threading
import time
import tkinter as tk
import webbrowser
from datetime import datetime
from tkinter import filedialog
from tkinter import messagebox, scrolledtext, simpledialog

import openai
import pyperclip
import requests
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from concurrent.futures import ThreadPoolExecutor
from tkinter import scrolledtext

# 禁用urllib3的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_expiration_date():
    # 设置软件过期日期
    expiration_date = datetime(2025, 12, 31)
    current_date = datetime.now()

    # 检查当前日期是否超过过期日期
    if current_date > expiration_date:
        # 创建一个Tkinter根窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口

        # 弹出消息框让用户选择
        result = messagebox.askquestion("软件过期", "软件已过期，请联系作者:84406570@qq.com\n或者选择输入秘钥解锁",
                                        icon='warning',
                                        type='yesno')

        if result == 'yes':
            # 用户选择“是”，打开默认邮件客户端让用户联系作者
            email_link = "mailto:author@example.com?subject=软件过期支持"
            root.destroy()  # 销毁Tkinter根窗口
            import webbrowser
            webbrowser.open(email_link)
        elif result == 'no':
            # 用户选择“否”，弹出输入框让用户输入秘钥
            root.destroy()  # 销毁Tkinter根窗口
            key = simpledialog.askstring("输入秘钥", "请输入您的解锁秘钥：")
            if key == "木木小辛":  # 替换YOUR_SECRET_KEY为实际的秘钥
                print("秘钥正确，软件已解锁。")
            else:
                print("秘钥错误，软件将退出。")
                exit()
        else:
            # 用户取消操作，退出程序
            root.destroy()
            exit()


# 在程序开始时调用时间检测函数
check_expiration_date()
# 全局变量
driver_instance = None
api_key_folder = "api_key"
api_key_file_openai = os.path.join(api_key_folder, "openai_api_key.txt")
api_key_file_zhipu = os.path.join(api_key_folder, "zhipu_api_key.txt")
api_choice_global = ""
base_url_zhipu = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
# 设置源语言和目标语言
source_lang = 'zh'
target_lang = 'en'
character_content="你的任务是提供专业、准确、有极高的深度、有极高的创新性、有丰富的细节、有洞察力、严谨证明、严格语言逻辑、提供更多相关专业背景、具体案例、具体思考过程、深入分析、提供具体的计算和设计细节建议,回答内容为word格式的,不要使用#或者*等符号作为段落的占位符。你的回答思考可以参考下面的方式但是不限于:是全面解读与分析：在回应之前，深入理解用户的问题，探索所有相关背景和上下文信息，确保全面捕捉问题的实质。多角度探索：从不同视角审视问题，考虑各种可能的解决方案，不局限于传统或直接的方法。详细步骤阐述：对于每个解决方案，详细描述其实施步骤，确保逻辑清晰，易于用户理解。自然思考流程：模拟人类的自然思考过程，从一个想法自然过渡到另一个，允许思维的漫游和创造性的连接。偏离与回归：在思考过程中允许适当的偏离，但能够适时将焦点引导回核心问题，保持回答的相关性。逐步深化理解：逐步构建对问题的理解，不急于求成，而是通过层层深入的分析来构建全面的回答。情感与逻辑融合：在回答中融入情感因素和逻辑分析，使回答更加人性化和有说服力。全面性提醒：始终保持思考的全面性，确保不遗漏用户消息的任何细节，捕捉所有可能的内涵。创造性见解：在思考过程中鼓励创造性思维，寻找新颖的解决方案和独到的见解。清晰表达：确保最终的回答清晰、准确，避免使用专业术语或复杂表达，使所有用户都能理解。情感共鸣：在回答中体现对用户情感的理解和共鸣，特别是在处理敏感或复杂问题时。文化和语境敏感性：在回答中考虑到文化差异和语境的重要性，确保回答对所有用户都是适宜和尊重的。持续学习和适应：表现出对新信息的适应性和学习能力，确保回答能够反映最新的知识和最佳实践。简洁而全面：在保持回答简洁的同时，确保覆盖所有关键点，避免冗余但不失全面性"
# 检查api_key文件夹是否存在，如果不存在则创建
if not os.path.exists(api_key_folder):
    os.makedirs(api_key_folder)

def read_api_key(file_path):
    """读取API密钥"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read().strip()
    return None

def write_api_key(file_path, key):
    """写入API密钥"""
    with open(file_path, 'w') as f:
        f.write(key)

def get_driver():
    """获取WebDriver实例"""
    global driver_instance
    if driver_instance is None:
        driver_instance = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver_instance
api_key_openai = read_api_key(api_key_file_openai)
api_key_zhipu = read_api_key(api_key_file_zhipu)

def get_user_agent_from_website():
    """获取User-Agent字符串"""
    url = 'https://www.useragentstring.com/'
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        uas_textarea = soup.find('textarea', {'name': 'uas', 'id': 'uas_textfeld'})
        if uas_textarea:
            return uas_textarea.text.strip()
        else:
            raise Exception("无法从网站获取User-Agent字符串。")
    except requests.RequestException as e:
        messagebox.showerror("错误", f"请求User-Agent网站失败：{e}")
        sys.exit()

def get_openai_base_url():
    """动态获取OpenAI的base_url"""
    user_agent = get_user_agent_from_website()
    if not user_agent:
        sys.exit()
    github_url = 'https://github.com/popjane/free_chatgpt_api'
    soup = analyze_webpage(github_url, user_agent)
    if not soup:# 无法获取网页内容
        sys.exit()

    free_key_link = soup.find('a', string='立即领取免费KEY')
    if not free_key_link or not free_key_link.has_attr('href'):
        messagebox.showerror("错误", "无法找到免费KEY的链接。")
        sys.exit()
    free_key_url = free_key_link['href'].replace("&quot;", "").strip('"')
    if not free_key_url.startswith(('http://', 'https://')):
        free_key_url = 'https://' + free_key_url
    return free_key_url.replace("/github", "/v1/")  # 动态获取base_url

def analyze_webpage(url, user_agent):
    """分析网页"""
    headers = {
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        messagebox.showerror("错误", f"请求网页失败：{e}")
        return None
def get_openai_key_and_base_url(root):
    """获取OpenAI的API KEY和base_url"""
    global api_key, base_url
    base_url=get_openai_base_url()
    free_keys_url=base_url.replace( "/v1/","/github",)
    messagebox.showinfo("提示", "接下来登录你的github账号,如果没有请注册后登录完成KEY的领取")
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    driver.maximize_window()
    driver.get(free_keys_url)  # 直接使用获取到的 BASE URL
    api_key = simpledialog.askstring("输入", "请输入你的API KEY(例子sk-psMPDOC00000)：", parent=root)
    if api_key:
        print(f"API KEY: {api_key}")
        print(f"API URL: {base_url}")
        messagebox.showinfo("成功", "API KEY和API URL已成功获取。")
        write_api_key(api_key_file_openai, api_key)  # 保存API key到文件
    else:
        messagebox.showerror("错误", "API KEY为空，请重新获取。")
        sys.exit()
    driver.quit()

def check_and_get_zhipu_api_key(root):
    """检查并获取智谱AI的API KEY"""
    global api_key
    if not os.path.exists(api_key_folder):
        os.makedirs(api_key_folder)
        api_key = ""
    else:
        if os.path.exists(api_key_file_zhipu):
            with open(api_key_file_zhipu, 'r') as file:
                api_key = file.read().strip()
        else:
            api_key = ""
    if not api_key:
        webbrowser.open('https://open.bigmodel.cn/usercenter/apikeys')
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        result = simpledialog.askstring("注册API Key", '请在网页中注册API Key并将其粘贴到这里：', parent=root)
        if result:
            write_api_key(api_key_file_zhipu, result)  # 保存API key到文件
            api_key = result
        else:
            print("用户取消注册，程序退出。")
            exit()

def set_api_key_and_base_url(key, url):
    """设置API密钥和基础URL"""
    global api_key, base_url
    api_key = key
    base_url = url
    print(f"API KEY: {api_key}")
    print(f"API URL: {base_url}")
    messagebox.showinfo("成功", "API KEY和API URL已成功获取。")

def get_response(user_message):
    try:
        call_get_response(user_message)
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("错误", f"处理响应时发生错误：{e}"))
# 新增一个函数，用于在子线程中调用get_response
def get_response_async(user_message):
    threading.Thread(target=get_response, args=(user_message,)).start()
# 在UI中调用
def on_entry_key(event):
    if event.keysym == "Return":
        start_loading()
        user_message = entry.get()
        get_response_async(user_message)  # 使用异步方式处理长字符串
        entry.delete(0, tk.END)
def select_api(api_choice, root):
    global api_choice_global, api_key_openai, api_key_zhipu, base_url_zhipu
    api_choice_global = api_choice
    if api_choice == "openai":
        # 检查本地是否存在 OpenAI 的 API Key
        api_key_openai = read_api_key(api_key_file_openai)
        if not api_key_openai:
            get_openai_key_and_base_url(root)
        openai.api_key = api_key_openai
        openai.base_url = get_openai_base_url()
        print("openai")  # 添加打印语句
    elif api_choice == "zhipu":
        # 检查本地是否存在 智谱AI 的 API Key
        api_key_zhipu = read_api_key(api_key_file_zhipu)
        if not api_key_zhipu:
            check_and_get_zhipu_api_key(root)
        openai.api_key = api_key_zhipu
        openai.base_url = base_url_zhipu
        print("zhipu")  # 添加打印语句
    else:
        messagebox.showerror("错误", "未选择AI服务提供商")
        #结束进程
        exit()
    # 关闭窗口
    root.destroy()
    return openai.api_key, openai.base_url if api_choice == "openai" else api_key_zhipu, openai.base_url
聊天记录保存 = []
最后的答案 = ""

def get_response_openai(user_message):
    """获取AI的回答（OpenAI）"""
    global 聊天记录保存, 最后的答案,character_content
    if user_message.strip():
        聊天记录保存.append({"role": "assistant", "content": user_message})
        if len(聊天记录保存) > 100:
            聊天记录保存.pop(0)
        try:
            model = "gpt-4o-mini"  # 此处假设模型选择固定为"gpt-4o-mini"
            ai_message = user_message  # 此处简化处理，实际情况可能需要根据模型选择进行调整
            completion = openai.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": f"提示词:{character_content}"
                    },
                    {
                        "role": "system",
                        "content": f"上下文:{聊天记录保存}"
                    },
                    {
                        "role": "user",
                        "content": ai_message
                    }
                ],
            )
            response = completion.choices[0].message.content
            最后的答案 = response
            聊天记录保存.append({"role": "assistant", "content": response})
            root.after(0, lambda: finish_loading(response, user_message))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("错误", f"发生错误：{e}"))
def get_response_zhipu(user_message):
    """获取AI的回答（智谱AI）"""
    global 聊天记录保存, 最后的答案,character_content
    if user_message.strip():
        聊天记录保存.append({"role": "assistant", "content": user_message})
        if len(聊天记录保存) > 100:
            聊天记录保存.pop(0)
        try:
            headers = {
                "Authorization": f"Bearer {openai.api_key}",
                "Content-Type": "application/json"
            }
            system_message = {
                "role": "system",
                "content": f"提示词:{character_content}"
            }
            sxw_message = {
                "role": "system",
                "content":f"上下文:{聊天记录保存}"
            }
            payload = {
                "model": "GLM-4-Flash",  # 确保这是您想要使用的模型
                "messages": [system_message,sxw_message, {"role": "user", "content": user_message}]
            }
            response = requests.post(openai.base_url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
            最后的答案 = response_data["choices"][0]["message"]["content"]
            聊天记录保存.append({"role": "assistant", "content": 最后的答案})
            root.after(0, lambda: finish_loading( 最后的答案,user_message))
        except Exception as e:
            root.after(0, lambda e: messagebox.showerror("错误", f"发生未知错误：{e}"))

def call_get_response(user_message):
    global api_choice_global
    entry.delete(0, tk.END)
    if api_choice_global == "openai":
        return get_response_openai(user_message)
    elif api_choice_global == "zhipu":
        return get_response_zhipu(user_message)

def finish_loading(response,问题):
    def update_ui():
        output.config(state="normal")
        output.insert(tk.END, f"我:{问题}\n")
        output.insert(tk.END, f"Ai: ---------------------﹀--------------------------\n {response}\n------------------------︿--------------------------\n")
        output.config(state="disabled")
        output.see(tk.END)
        update_status("就绪")
    root.after(0, update_ui)
# 创建主窗口
root = tk.Tk()
root.title("选择AI服务提供商")
root.geometry("300x200")
# 创建一个标签
label = tk.Label(root, text="请选择AI服务提供商：")
label.pack(pady=10)

# 创建一个Frame来放置OpenAI的按钮和提示框
frame_openai = tk.Frame(root)
frame_openai.pack(pady=5)

# 创建OpenAI的按钮，并放入frame_openai中
button_openai = tk.Button(frame_openai, text="OpenAI", command=lambda: select_api("openai", root))
button_openai.pack(side=tk.LEFT, padx=10)
# 创建OpenAI的提示框，并放入frame_openai中
label_openai = tk.Label(frame_openai, text="OpenAI的gpt-4o-mini模型\n需要github账号进行获取Key")
label_openai.pack(side=tk.LEFT)

# 创建一个Frame来放置智谱AI的按钮和提示框
frame_zhipu = tk.Frame(root)
frame_zhipu.pack(pady=5)

# 创建智谱AI的按钮，并放入frame_zhipu中
button_zhipu = tk.Button(frame_zhipu, text="智谱AI", command=lambda: select_api("zhipu", root))
button_zhipu.pack(side=tk.LEFT, padx=10)
# 创建智谱AI的提示框，并放入frame_zhipu中
label_zhipu = tk.Label(frame_zhipu, text="智谱AI的GLM-4-Flash模型\n需要注册账号进行获取Key")
label_zhipu.pack(side=tk.LEFT)

# 创建取消按钮
button_cancel = tk.Button(root, text="取消", command=lambda: select_api("", root))
button_cancel.pack(pady=5)

# 运行tkinter主循环
root.mainloop()
def start_loading():
    """显示加载中提示框"""
    update_status("正在加载...")

def clear_conversation():
    """清除对话"""
    global 聊天记录保存
    聊天记录保存 = []  # 直接重置列表，而不是删除元素，以释放内存
    output.config(state="normal")
    output.delete(1.0, tk.END)
    output.config(state="disabled")
    output.see(tk.END)

# 搜索Metaso
def search_metaso(query):
    try:
        driver = get_driver()
        driver.maximize_window()
        driver.get("https://metaso.cn/")
        # 等待搜索框加载完成
        driver.implicitly_wait(2)

        search_box = driver.find_element(By.CSS_SELECTOR, 'textarea.search-consult-textarea')
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)

    except TimeoutException:
        messagebox.showerror("错误", "页面加载超时，请检查网络连接或网址是否正确。")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")

def save_conversation():
    """保存对话"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("聊天记录保存.txt", "a", encoding="utf-8") as f:
        f.write(f"保存时间: {timestamp}\n")
        for entry in 聊天记录保存:
            role = entry["role"]
            content = entry["content"]
            f.write(f"{role}: {content}\n")
        f.write("\n")
    messagebox.showinfo("保存成功", "对话已保存到 聊天记录保存.txt")

def load_last_conversation():
    """加载上次对话"""
    try:
        with open("聊天记录保存.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            output.config(state="normal")
            output.delete(1.0, tk.END)
            for line in lines:
                output.insert(tk.END, line)
            output.config(state="disabled")
    except Exception as e:
        messagebox.showerror("错误", f"加载失败：{e}")

def get_response_async(user_message):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(get_response, user_message)
        return future.result()


# 在UI中调用
def on_entry_key(event):
    if event.keysym == "Return":
        start_loading()
        threading.Thread(target=get_response_async, args=(entry.get(),)).start()
        entry.delete(0, tk.END)

def copy_last_answer():
    """复制最后回答"""
    global 最后的答案
    if 最后的答案:
        pyperclip.copy(最后的答案)
        messagebox.showinfo("复制成功", "已复制到剪贴板！")
    else:
        messagebox.showwarning("警告", "没有可复制的回答！")

# 增加复制并跳转到PPT生成页面的功能
def copy_and_open_ppt():
    global 最后的答案
    if 最后的答案:
        pyperclip.copy(最后的答案)
        messagebox.showinfo("复制成功", "准备跳转到PPT设计网页！")
        # 使用 Selenium 打开指定网页并粘贴内容
        driver = get_driver()
        driver.maximize_window()
        driver.get("https://kimi.moonshot.cn/kimiplus/conpg18t7lagbbsfqksg")
        time.sleep(5)
        editable_div = driver.find_element(By.ID, "msh-chateditor")
        editable_div.send_keys(Keys.CONTROL, 'v')
        editable_div.click()

    else:
        messagebox.showwarning("警告", "没有可复制的回答！")

# 增加复制并跳转到思维导图生成页面的功能
def copy_and_open_mindmap():
    global 最后的答案
    if 最后的答案:
        pyperclip.copy(最后的答案)
        messagebox.showinfo("复制成功", "准备生成思维导图！")
        # 使用 Selenium 打开思维导图页面并粘贴内容
        driver = get_driver()
        driver.maximize_window()
        driver.get("https://app.amymind.com/mindmap/guide")
        try:
            element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//h2[text()='粘贴文本']/.."))
            )
            element.click()
            textarea = driver.find_element(By.ID, "paste-form_content")
            textarea.click()
            textarea.send_keys(Keys.CONTROL, 'v')
        except TimeoutException:
            messagebox.showerror("错误", "等待粘贴文本区域超时，请重试。")
            return
        generate_button = driver.find_element(By.XPATH, "//button[span[text()='生 成']]")
        generate_button.click()

    else:
        messagebox.showwarning("警告", "没有可复制的回答！")

# 提取Mermaid代码的函数
def extract_content(text, start_marker="```mermaid", end_marker="```"):
    start_index = text.find(start_marker) + len(start_marker)
    if start_index == -1:
        return "Start marker not found."

    end_index = text.rfind(end_marker)
    if end_index == -1:
        return "End marker not found."

    if start_index >= end_index:
        return "Invalid markers order."

    extracted_content = text[start_index:end_index].strip()
    return extracted_content
# 增加复制并跳转到流程图生成页面的功能
def convert_to_mermaid_and_copy():
    global 最后的答案
    if 最后的答案:
        update_status("正在生成Mermaid流程图...")
        try:
            # 根据api_choice_global的值选择不同的处理方式
            if api_choice_global == "openai":
                result = call_model_for_mermaid_openai(最后的答案)
            elif api_choice_global == "zhipu":
                result = call_model_for_mermaid_zhipu(最后的答案)
            else:
                messagebox.showerror("错误", "未知的API服务提供商")
                return

            pyperclip.copy(result)
            messagebox.showinfo("复制成功", "准备跳转到流程图设计网页！\n使用方法等待网页完全打开后会自动粘贴内容")
            open_process_diagram_page()
            update_status("完成")
        except Exception as e:
            messagebox.showerror("错误", f"请求或处理Mermaid代码时发生错误：{e}")
    else:
        messagebox.showwarning("警告", "没有可复制的回答！")

def call_model_for_mermaid_openai(user_message):
    # 使用OpenAI模型获取Mermaid代码
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"要求将内容转化成为Mermaid代码,不能够删减内容,并且输出的只有语法相关的,其他的对白均不需要: {user_message}"}],
    )
    results = completion.choices[0].message.content
    return extract_content(results)

def call_model_for_mermaid_zhipu(user_message):
    # 使用智谱AI模型获取Mermaid代码
    headers = {"Authorization": f"Bearer {api_key_zhipu}", "Content-Type": "application/json"}
    payload = {
        "model": "GLM-4-Flash",  # 假设使用的是这个模型
        "messages": [{"role": "user", "content": f"要求将内容转化成为Mermaid代码,不能够删减内容,并且输出的只有语法相关的,其他的对白均不需要: {user_message}"}]
    }
    response = requests.post(base_url_zhipu, headers=headers, json=payload)
    response.raise_for_status()
    response_data = response.json()
    return extract_content(response_data["choices"][0]["message"]["content"])

def open_process_diagram_page():
    # 打开流程图设计网页并粘贴Mermaid代码
    try:
        driver = get_driver()
        driver.maximize_window()
        driver.get("https://excalidraw.com/")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="dropdown-menu-button"]')))
        more_tools_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="dropdown-menu-button"]')
        more_tools_button.click()
        time.sleep(1)
        button = driver.find_element(By.XPATH, "//button[contains(.//text(), 'Mermaid 至 Excalidraw')]")
        button.click()
        time.sleep(1)
        textarea = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea.ttd-dialog-input')))
        textarea.clear()
        textarea.send_keys(Keys.CONTROL, 'v')
        time.sleep(10)
    except Exception as e:
        messagebox.showerror("错误", f"打开流程图设计网页时发生错误：{e}")

def xssearch_metas(query):
    """执行学术搜索"""
    try:
        driver = get_driver()
        driver.maximize_window()
        driver.get("https://qa.citexs.com/")
        input_element = driver.find_element(By.CSS_SELECTOR, ".el-input__inner")
        input_element.clear()
        input_element.send_keys(query)
        input_element.send_keys(Keys.RETURN)
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")


def download_image(img_url, folder_name, index,  lock):#
    try:
        img_data = requests.get(img_url).content
        with open(os.path.join(folder_name, f"{index + 1}.jpg"), "wb") as f:
            f.write(img_data)
        with lock:
            print(f"已下载图片：{index + 1}.jpg")
    except Exception as e:
        with lock:
            print(f"下载图片时出错：{e}")
            root.after(0, lambda: update_status("下载出错"))

def get_image_count(folder_name):
    # 获取文件夹中图片的数量
    return len([name for name in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, name))])


def scroll_to_load_more(driver, scroll_times=10, scroll_amount=500, wait_time=1): #模拟逐步滚动以加载更多内容
    """
    参数:
        driver: Selenium WebDriver 对象
        scroll_times: 想要滚动的次数
        scroll_amount: 每次滚动的像素值
        wait_time: 每次滚动后等待的时间，以便页面加载更多内容
    """
    for _ in range(scroll_times):        # 执行逐步滚动的脚本
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")        # 等待一段时间，让页面加载内容
        time.sleep(wait_time)

    # scroll_to_load_more(driver, scroll_times=10, scroll_amount=500, wait_time=2)
    time.sleep(1)  # 等待页面加载，可能需要调整等待时间
def 翻译(api_choice_global,search_term):
    if api_choice_global == "openai":
        # 检查本地是否存在 OpenAI 的 API Key
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"{search_term}用英语翻译一下, 并且只要回答我单词就行"}],
        )
        results = completion.choices[0].message.content
    elif api_choice_global == "zhipu":
        # 检查本地是否存在 智谱AI 的 API Key
        headers = {
            "Authorization": f"Bearer {openai.api_key}",
            "Content-Type": "application/json"
        }
        system_message = {
            "role": "system",
            "content": "你是一个乐于回答各种问题的小助手，你的任务是提供专业、准确、有洞察力的建议。"
        }
        payload = {
            "model": "GLM-4-Flash",  # 确保这是您想要使用的模型
            "messages": [system_message, {"role": "user", "content": f"{search_term}用英语翻译一下, 并且只要回答我单词就行"}]
        }
        response = requests.post(openai.base_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        results = result["choices"][0]["message"]["content"]
    return results

def search_images(result,是否下载, on_complete=None):
    global api_choice_global
    results = 翻译(api_choice_global, result)
    print(results)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))#最大化后最小化
    if 是否下载=="yes":
        driver.minimize_window()
    else:
        driver.maximize_window()
    driver.get(f"https://pixabay.com/images/search/{results}/")
    driver.implicitly_wait(10)
    if on_complete:# 检查回调是否存在
        on_complete(driver)  # 调用回调函数
    return driver,results


def download_images(search_term, number_of_images):
    def download():
        global xz
        quantity = int(number_of_images)
        folder_name = search_term + "的图片"
        翻页次数 = math.ceil(quantity / 3)
        print(翻页次数)
        result = messagebox.askquestion("确认",
                                        f"请确认是否开始下载{quantity}张{folder_name}?\n大约需要{56+翻页次数}秒\n请注意在下载过程中不要关闭浏览器!")
        if result == "yes" and quantity > 0:
            xz = 1  # 下载图片
            entry.delete(0, tk.END)
            if not os.path.exists(folder_name):  # 如果文件夹不存在，则创建
                os.makedirs(folder_name)
            def download_images_in_background(search_term, quantity, folder_name):
                try:
                    driver,results = search_images(search_term,"yes")# 搜索图片

                    scroll_to_load_more(driver, scroll_times=翻页次数, scroll_amount=900, wait_time=1)# 滚动加载更多图片
                    img_elements = driver.find_elements(By.CSS_SELECTOR, "img[src]")
                    nimg_elements = img_elements[4:-6]
                    print(f"找到 {len(nimg_elements)} 个图片元素。")
                    #如果len(nimg_elements)大于quantity则
                    if len(nimg_elements) > quantity:
                        nimg_element = nimg_elements[:quantity]
                    else:
                        nimg_element = nimg_elements
                    print(f"将下载 {len(nimg_element)} 张图片。")
                    lock = threading.Lock()
                    t = get_image_count(folder_name)  # 获取文件夹中已有的图片数量
                    threads = []
                    for index, img_element in enumerate(nimg_element):
                        img_url = img_element.get_attribute("src")
                        thread_index = index + t  # 从已有图片数量开始命名
                        thread = threading.Thread(target=download_image, args=(img_url, folder_name, thread_index, lock))
                        threads.append(thread)
                        thread.start()

                    for thread in threads:
                        thread.join()
                    driver.quit()
                    messagebox.showinfo("提示", f"图片下载完成，请查看{folder_name}文件夹。")
                    if os.name == 'nt':
                        os.startfile(folder_name)
                    elif os.name == 'posix':
                        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                        subprocess.run([opener, folder_name])
                except Exception as e:
                    print(f"发生错误：{e}")
            threading.Thread(target=download_images_in_background, args=(search_term, quantity, folder_name)).start()
        else:
            messagebox.showinfo("提示", "已取消下载图片。")
    #关闭页面
    xz = 0
    threading.Thread(target=download).start()
    update_status("就绪")


def validate_spinbox(value):
    """验证Spinbox输入"""
    if value == "":
        return True
    try:
        num = int(value)
        if 0 <= num <= 100:
            return True
    except ValueError:
        pass
    return False


def on_spinbox_validate(spinbox, value):
    """处理Spinbox验证"""
    if not validate_spinbox(value):
        values = spinbox['values']
        if values:
            current_value = spinbox.get()
            closest_value = min(values, key=lambda x: abs(int(x) - int(current_value)))
            spinbox.delete(0, "end")
            spinbox.insert(0, closest_value)
        return False
    return True


# 根据xz的值更新hint_label2的文本
def update_hint_label2(xz):
    if xz:
        hint_label2.config(text="下载中，请等待...")
    else:
        hint_label2.config(text="请在输入框中填写您要下载的图片(1-99)张\n点击按键下载到本地的'xx的图片'文件夹中")


# 处理撤回和重做
undo_stack = []
redo_stack = []


def undo():
    """撤回操作"""
    if undo_stack:
        entry.delete(0, tk.END)
        entry.insert(0, undo_stack.pop())
        redo_stack.append(entry.get())


def redo():
    """重做操作"""
    if redo_stack:
        entry.delete(0, tk.END)
        entry.insert(0, redo_stack.pop())
        undo_stack.append(entry.get())


def on_entry_key(event):
    """处理输入框键盘事件"""
    if event.keysym == "Return":
        start_loading()
        threading.Thread(target=get_response, args=(entry.get(),)).start()
        entry.delete(0, tk.END)
    elif event.keysym == "z" and event.state & 0x0004:  # Ctrl+Z
        undo()
    elif event.keysym == "y" and event.state & 0x0004:  # Ctrl+Y
        redo()
    else:
        if entry.get():
            undo_stack.append(entry.get())

def select_file():
    global character_content
    file_path = filedialog.askopenfilename(
        title="默认模型(TXT)",
        filetypes=[("Text files", "*.txt")]
    )
    if file_path:
        # 更新按钮文本为文件名
        select_button.config(text=os.path.basename(file_path)[:-4])
        with open(file_path, 'r', encoding='utf-8') as file:
            character_content = file.read()




# 创建主窗口
#如果api_choice_global 不等于空则运行后面的程序
if api_choice_global != "":
    root = tk.Tk()
    root.title("MMXX AI 2.7")
    root.geometry("800x580")
    root.configure(bg="#f0f0f0")
else:
    #结束进程
    sys.exit()

# 创建输出框，使用grid布局管理器，并设置weight属性
output = scrolledtext.ScrolledText(root, state="disabled", bg="#ffffff", font=("微软雅黑", 10))
output.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # sticky="nsew" 使输出框填充整个单元格

# 配置grid布局管理器的行和列的权重
root.grid_rowconfigure(0, weight=1)  # 设置行权重
root.grid_columnconfigure(0, weight=1)  # 设置列权重

# 输入框和按钮的框架
frame = tk.Frame(root, bg="#f0f0f0")
frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)  # 使用grid而不是pack

# 创建一个按钮，点击后弹出文件选择对话框
select_button = tk.Button(frame, text="模型描述TXT", command=select_file, bg="#f44336", fg="white", font=("微软雅黑", 10))
select_button.grid(row=0, column=0, padx=5)  # 使用grid而不是pack

# 输入框
entry = tk.Entry(frame, width=55, font=("微软雅黑", 12))
entry.grid(row=0, column=1, padx=5)  # 使用grid而不是pack
entry.bind("<Key>", on_entry_key)

# 发送按钮
send_button = tk.Button(frame, text="AI对话", command=lambda: [start_loading(), threading.Thread(target=get_response,args=(entry.get(),)).start()],
                        bg="#4CAF50", fg="white", font=("微软雅黑", 10))
send_button.grid(row=0, column=2, padx=5)  # 使用grid而不是pack

# 创建搜索按钮
search_button = tk.Button(frame, text="搜索", command=lambda: search_metaso(entry.get()) if entry.get() else None,
                          bg="#4CAF50", fg="white", font=("微软雅黑", 10))
search_button.grid(row=0, column=3, padx=5)  # 使用grid而不是pack

# 创建学术搜索按钮
academic_search_button = tk.Button(frame, text="学术", command=lambda: xssearch_metas(entry.get())if entry.get() else None,
                          bg="#4CAF50", fg="white", font=("微软雅黑", 10))
academic_search_button.grid(row=0, column=4, padx=5)  # 使用grid而不是pack

# 创建提示标签
hint_label = tk.Label(root, text="提示:模型的选择会让AI的输出有侧重点>>>提示:下面的紫色按键功能只会针对最后一次的回答进行处理>>>提示: 按'Enter'可直接让AI输出", bg="#f0f0f0", font=("微软雅黑", 8))
hint_label.grid(row=2, column=0, sticky="ew", padx=5, pady=2)  # 使用grid而不是pack

# 功能按钮框架
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)  # 使用grid而不是pack

# 清除按钮
clear_button = tk.Button(button_frame, text="清除对话", command=clear_conversation, bg="#f44336", fg="white", font=("微软雅黑", 10))
clear_button.grid(row=1, column=0, padx=5)  # 使用grid而不是pack

# 保存按钮
save_button = tk.Button(button_frame, text="保存对话", command=save_conversation, bg="#2196F3", fg="white", font=("微软雅黑", 10))
save_button.grid(row=1, column=1, padx=5)  # 使用grid而不是pack

# 加载按钮
load_button = tk.Button(button_frame, text="加载对话", command=load_last_conversation, bg="#FF9800", fg="white", font=("微软雅黑", 10))
load_button.grid(row=0, column=0, padx=5)  # 使用grid而不是pack

# 复制按钮
copy_button = tk.Button(button_frame, text="复制回答", command=copy_last_answer, bg="#9C27B0", fg="white", font=("微软雅黑", 10))
copy_button.grid(row=0, column=1, padx=5)  # 使用grid而不是pack

# 生成PPT按钮
ppt_button = tk.Button(button_frame, text="生成PPT", command=copy_and_open_ppt, bg="#673AB7", fg="white", font=("微软雅黑", 10))
ppt_button.grid(row=0, column=4, padx=5)  # 使用grid而不是pack

# 生成思维导图按钮
mindmap_button = tk.Button(button_frame, text="生成思维导图", command=copy_and_open_mindmap, bg="#673AB7", fg="white", font=("微软雅黑", 10))
mindmap_button.grid(row=0, column=5, padx=5)  # 使用grid而不是pack

# 新增按钮：转换为Mermaid流程图语法
mermaid_button = tk.Button(button_frame, text="生成流程图", command=convert_to_mermaid_and_copy, bg="#673AB7", fg="white", font=("微软雅黑", 10))
mermaid_button.grid(row=0, column=6, padx=5)  # 使用grid而不是pack

# 创建一个Spinbox组件，允许选择1到100之间的数字
number_spinbox = tk.Spinbox(button_frame, from_=1, to=99, width=3, font=("微软雅黑", 12), validate='all', validatecommand=(root.register(validate_spinbox), '%P'))
number_spinbox.grid(row=0, column=7, padx=5)  # 使用grid而不是pack

# 创建下载图片的按钮
st_button = tk.Button(button_frame, text="下图", command=lambda: download_images(entry.get(), number_spinbox.get()) if entry.get() else None, bg="#B22222", fg="white", font=("微软雅黑", 10))
st_button.grid(row=0, column=8, padx=5)  # 使用grid而不是pack

def on_search_images_click():# 搜索图片的函数
    search_term = entry.get()
    if search_term:
        是否下载 = "No"
        threading.Thread(target=lambda: search_images(search_term,是否下载)).start()# 启动线程执行搜索图片的操作
        是否下载="Yes"
    else:
        messagebox.showwarning("警告", "请输入搜索关键词！")


# 创建下载图片的按钮
st_button = tk.Button(button_frame, text="搜图", command=on_search_images_click , bg="#B22222", fg="white", font=("微软雅黑", 10))
st_button.grid(row=0, column=9, padx=5)  # 使用grid而不是pack

# 创建提示标签
hint_label2 = tk.Label(button_frame, text="请在输入框中填写您要下载的图片(1-99)张\n点击按键下载到本地的'xx的图片'文件夹中", bg="#f0f0f0", font=("微软雅黑", 8))
hint_label2.grid(row=0, column=10, columnspan=10, padx=5, pady=5)  # 使用grid而不是pack

# 创建状态栏
status_frame = tk.Frame(root, bg="#f0f0f0", height=20)
status_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=5)  # 使用grid而不是pack

# 创建状态栏上的标签
status_label = tk.Label(status_frame, text="就绪", font=("微软雅黑", 10), anchor="w")
status_label.pack(side="left", padx=5)  # 状态栏使用pack

# 更新状态栏的函数
def update_status(message):
    root.after(0, lambda: status_label.config(text=message))

# 运行tkinter主循环
root.mainloop()
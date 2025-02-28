# AI-2.7
“一个功能强大的 AI 驱动应用程序，具有多种实用功能。该程序集成了基于 AI 的聊天功能，支持 OpenAI 和智谱 AI 等不同模型，能够进行智能对话和问题解答。此外，它还具备图片下载与处理功能，用户可以根据搜索关键词下载相关图片。程序还支持将对话内容生成 PPT 和思维导图，方便用户进行进一步的展示和分析。同时，它还集成了网页搜索和学术搜索功能，帮助用户获取更多信息。该应用程序拥有用户友好的图形界面，使用户能够轻松地与 AI 进行交互，管理对话记录，并高效地执行各种任务。它还支持 AI 模型的自定义设置，并且具有撤销和重做用户输入的功能。”
## 软件说明

### 概述

MMXX AI 2.7 是一款综合性的人工智能驱动应用程序，旨在为用户提供广泛的人工智能服务。它集成了多种先进技术和服务，方便用户执行各种任务，如基于 AI 的聊天、图片处理、内容生成和信息搜索。

### 功能

  1. **AI 聊天** ：支持与不同的 AI 模型（包括 OpenAI 和智谱 AI）进行聊天。用户可以与 AI 进行智能对话并获得问题的答案。聊天记录会被保存，用户可以对其进行管理。
  2. **图片下载和处理** ：用户可以根据关键词搜索图片并下载。应用程序可以处理一定数量的图片，并将其保存到指定的文件夹中。它还具有搜索图片并显示结果的功能。
  3. **内容生成** ：可以根据对话内容生成 PPT 和思维导图。它为用户提供了创建视觉演示文稿和通过思维导图组织想法的便利。
  4. **网页搜索和学术搜索** ：集成了网页搜索和学术搜索功能。用户可以搜索网络上的信息和学术资源，以获取更多相关和深入的知识。
  5. **用户友好的界面** ：具有易于使用的图形用户界面（GUI）。用户可以通过直观的界面与 AI 进行交互、管理对话并执行各种任务。
  6. **自定义** ：允许用户根据自己的需求自定义 AI 模型并设置一些参数。它还具有撤销和重做用户输入的功能，以提升用户体验。

### 技术细节

  * **编程语言** ：使用 Python 开发，使用了多种库和框架，如用于 GUI 的 Tkinter、用于网页操作的 Selenium 和用于 HTTP 请求的 requests。
  * **AI 集成** ：连接到 OpenAI 和智谱 AI 的 API，以访问其强大的语言模型，用于聊天和内容生成功能。
  * **图片处理** ：使用基于网页的图片搜索和下载方法，并可以通过 Selenium 处理网页上的图片元素。

### 系统要求

  * **操作系统** ：兼容 Windows、macOS 和 Linux 操作系统。
  * **Python 版本** ：需要 Python 3.x 版本来运行。
  * **依赖项** ：依赖于多个 Python 库，如 openai、selenium、requests、BeautifulSoup 等。这些依赖项可以通过 pip 包管理器安装。

### 安装和使用

  1. **安装 Python** ：确保您的系统已安装 Python。如果没有，请从 Python 官方网站下载并安装。
  2. **安装依赖项** ：打开命令行或终端，导航到应用程序文件所在的目录。然后运行命令`pip install -r requirements.txt`来安装所有所需的 Python 库。
  3. **运行应用程序** ：执行主 Python 脚本`MMXX AI 2.7.py`，使用命令`python MMXX AI 2.7.py`。应用程序将启动，并显示主界面。
  4. **配置 API 密钥** ：如果您想使用 AI 聊天功能，需要从 OpenAI 或智谱 AI 获取 API 密钥，并按照代码中的说明在应用程序中进行配置。
  5. **开始使用** ：应用程序启动并配置完成后，您可以通过图形界面使用各种功能，如 AI 聊天、图片下载、内容生成和网页搜索。

### 注意事项

  * **API 密钥管理** ：AI 服务的 API 密钥应妥善保管，不要与他人共享。使用 AI 提供商的 API 时，务必遵守其服务条款。
  * **互联网连接** ：应用程序的某些功能（如网页搜索、图片下载和 AI 聊天）需要互联网连接才能正常工作。
  * **合法和道德使用** ：用户应遵守法律法规和道德标准使用应用程序。不要将其用于任何非法或不当目的。

## README

# MMXX AI 2.7 使用说明书

## 简介

MMXX AI 2.7 是一款多功能的人工智能应用程序，结合了人工智能的强大功能和用户友好的界面设计，为用户提供高效便捷的体验。

## 功能

### AI 聊天

  * **多模型支持** ：支持与 OpenAI 和智谱 AI 模型进行聊天。用户可以选择所需的模型进行智能对话并获得准确且有帮助的答案。
  * **聊天记录管理** ：聊天记录会被保存并显示在界面上。用户可以清除对话、将对话保存到文件中或加载上次的对话。

### 图片下载和处理

  * **图片搜索** ：用户可以输入关键词搜索网页上的图片。应用程序将显示搜索结果，并允许用户查看图片。
  * **图片下载** ：用户可以指定要下载的图片数量，应用程序将把图片下载到本地文件夹中。下载的图片可以轻松访问和使用。

### 内容生成

  * **PPT 生成** ：基于对话内容，应用程序可以生成 PPT。用户可以复制内容并将其粘贴到 PPT 设计网页中，创建专业的演示文稿。
  * **思维导图生成** ：可以生成思维导图，帮助用户组织和可视化想法。可以通过将内容粘贴到思维导图生成网页中来创建思维导图。

### 网页搜索和学术搜索

  * **网页搜索** ：集成了网页搜索功能，允许用户搜索网络上的信息。用户可以输入搜索词，应用程序将在浏览器中打开搜索结果页面。
  * **学术搜索** ：为用户提供了学术搜索功能，用于搜索学术论文和资源。这对于需要特定领域深入专业知识的用户非常有用。

## 系统要求

  * **操作系统** ：Windows、macOS 或 Linux
  * **Python 版本** ：3.x
  * **依赖项** ：

    * openai
    * selenium
    * requests
    * BeautifulSoup
    * urllib3
    * tkinter

## 安装

  1. 从 Python 官方网站安装 Python：<https://www.python.org/>
  2. 克隆仓库或下载应用程序文件
  3. 使用以下命令安装依赖项：
`pip install -r requirements.txt`
  4. 通过执行主脚本运行应用程序：
`python MMXX AI 2.7.py`

## 使用方法

  1. **AI 聊天** ：

     * 从界面中选择 AI 服务提供商（OpenAI 或智谱 AI）
     * 在输入框中输入您的消息并按回车键开始聊天
     * AI 的回复将显示在输出框中

  2. **图片下载** ：

     * 在输入框中输入图片的搜索关键词
     * 使用 Spinbox 指定要下载的图片数量
     * 点击 “下图” 按钮开始下载图片

  3. **内容生成** ：

     * 与 AI 进行对话后，点击 “生成 PPT” 或 “生成思维导图” 按钮生成相应的内容
     * 内容将被复制到剪贴板，您可以将其粘贴到相应的网页中创建 PPT 或思维导图

  4. **网页搜索和学术搜索** ：

     * 在输入框中输入搜索词
     * 点击 “搜索” 或 “学术” 按钮执行搜索
     * 搜索结果将在浏览器中显示

## 注意事项

  * 如果您想使用 AI 聊天功能，确保您已获得 AI 服务所需的 API 密钥。按照代码中的说明配置 API 密钥。
  * 妥善保管您的 API 密钥，不要与他人共享。
  * 应用程序的某些功能（如网页搜索、图片下载和 AI 聊天）需要互联网连接。
  * 使用应用程序时遵守法律法规和道德标准。

## 联系方式

如果您对应用程序有任何问题或疑问，请通过 84406570@qq.com 联系作者。
Software Description (软件说明)
软件描述
Overview (概述)
MMXX AI 2.7 is a comprehensive and multifunctional artificial intelligence - driven application designed to provide users with a wide range of intelligent services. It integrates various advanced technologies and tools to facilitate different tasks such as AI - based chat, image processing, content generation, and information search.  
Features (功能)
AI Chat ：Supports chat with different AI models including OpenAI and Zhipu AI. Users can have intelligent conversations and get answers to their questions. The chat history is saved and can be managed by users.
Image Download and Processing ：Users can search for images based on keywords and download them. The application can handle a certain number of images and save them to a specified folder. It also has functions to search for images and display the results.
Content Generation ：Can generate PPTs and mind maps based on the content of the conversation. It provides users with the convenience of creating visual presentations and organizing ideas through mind maps.
Web Search and Academic Search ：Integrates web search and academic search functions. Users can search for information on the web and academic resources to get more relevant and in - depth knowledge.
User - Friendly Interface ：Has a graphical user interface (GUI) that is easy to use. Users can interact with the AI, manage conversations, and perform various tasks through the intuitive interface.
Customization ：Allows users to customize AI models and set some parameters according to their needs. It also has features like undo and redo for user input to enhance the user experience.  
Technical Details (技术细节)
Programming Language ：Developed in Python, using various libraries and frameworks such as Tkinter for the GUI, Selenium for web operations, and requests for HTTP requests.
AI Integration ：Connects with OpenAI and Zhipu AI APIs to access their powerful language models for chat and content generation functions.
AI 集成：连接 OpenAI 和智谱 AI API，以访问其强大的语言模型，用于聊天和内容生成功能。
Image Processing ：Uses web - based image search and download methods, and can handle image elements on web pages through Selenium.  
System Requirements (系统要求)
Operating System ：Compatible with Windows, macOS, and Linux operating systems.
Python Version ：Requires Python 3.x version to run.
Dependencies ：Depends on several Python libraries such as openai, selenium, requests, BeautifulSoup, etc. These dependencies can be installed through the pip package manager.
Installation and Usage (安装和使用)
Install Python ：Make sure Python is installed on your system. If not, download and install it from the official Python website.
Install Dependencies ：Open the command line or terminal and navigate to the directory where the application files are located. Then run the commandpip install -r requirements.txtto install all the required Python libraries.
安装依赖：打开命令行或终端，导航到应用程序文件所在的目录。然后运行命令 pip install -r requirements.txt 安装所有必需的 Python 库。
Run the Application ：Execute the main Python scriptMMXX AI 2.7.pyusing the commandpython MMXX AI 2.7.py. The application will start, and the main interface will be displayed.
Configure API Keys ：If you want to use the AI chat functions, you need to obtain API keys from OpenAI or Zhipu AI and configure them in the application according to the instructions provided in the code.  
配置 API 密钥：如果您想使用 AI 聊天功能，您需要从 OpenAI 或智谱 AI 获取 API 密钥，并根据代码中提供的说明在应用程序中进行配置。
Start Using ：After the application is started and configured, you can use the various functions such as AI chat, image download, content generation, and web search through the graphical interface.
Notes (注意事项)
API Key Management ：The API keys for AI services should be kept secure and not shared with others. Make sure to follow the terms of service of the AI providers when using their APIs.
Internet Connection ：Some functions of the application such as web search, image download, and AI chat require an internet connection to work properly.
Legal and Ethical Use ：Users should use the application in accordance with the laws and regulations and ethical standards. Do not use it for any illegal or improper purposes.
MMXX AI 2.7 README
Introduction
MMXX AI 2.7 is a versatile AI - powered application that provides a wide range of functions to assist users in various tasks. It combines the power of artificial intelligence with user - friendly interface design to offer an efficient and convenient experience.
MMXX AI 2.7 是一款多功能的 AI 应用程序，提供各种功能以协助用户完成各种任务。它将人工智能的力量与用户友好的界面设计相结合，提供高效便捷的体验。
Features
AI Chat
Multi - model Support ：Supports chat with OpenAI and Zhipu AI models. Users can choose the desired model to have intelligent conversations and get accurate and helpful answers.
Chat History Management ：The chat history is saved and displayed in the interface. Users can clear the conversation, save the conversation to a file, or load the last conversation.
Image Download and Processing
Image Search ：Users can enter keywords to search for images on the web. The application will display the search results and allow users to view the images.
Image Download ：Users can specify the number of images to download and the application will download the images to a local folder. The downloaded images can be easily accessed and used.
Content Generation
PPT Generation ：Based on the content of the conversation, the application can generate PPTs. Users can copy the content and paste it into the PPT design webpage to create professional presentations.
Mind Map Generation ：Can generate mind maps to help users organize and visualize their ideas. The mind map can be created by pasting the content into the mind map generation webpage.
思维导图生成：可以生成思维导图，帮助用户组织和可视化他们的想法。思维导图可以通过将内容粘贴到思维导图生成网页上创建。
Web Search and Academic Search
Web Search ：Integrates a web search function that allows users to search for information on the web. Users can enter search terms and the application will open the search results page in the browser.
网络搜索：集成了网络搜索功能，允许用户在网络上搜索信息。用户可以输入搜索词，应用程序将在浏览器中打开搜索结果页面。
Academic Search ：Provides an academic search function for users to search for academic papers and resources. This is useful for users who need in - depth and professional knowledge in specific fields.
学术搜索：为用户提供学术论文和资源的搜索功能。这对于需要特定领域深入和专业知识的用户非常有用。
System Requirements
Operating System ：Windows, macOS, or Linux
Python Version ：3.x
Dependencies ：
openai
selenium
requests
BeautifulSoup
urllib3
tkinter
Installation
Install Python from the official website: https://www.python.org/
Clone the repository or download the application files
Install the dependencies using the following command:
pip install -r requirements.txt
Run the application by executing the main script:
python MMXX AI 2.7.py
Usage
AI Chat ：
Choose the AI service provider (OpenAI or Zhipu AI) from the interface
Enter your message in the input box and press Enter to start the chat
The AI response will be displayed in the output box
Image Download ：
Enter the search keyword for the image in the input box
Specify the number of images to download using the Spinbox
Click the "下图" (Download Image) button to start downloading the images
Content Generation ：
After having a conversation with the AI, click the "生成PPT" (Generate PPT) or "生成思维导图" (Generate Mind Map) button to generate the corresponding content
The content will be copied to the clipboard and you can paste it into the corresponding webpage to create the PPT or mind map
Web Search and Academic Search ：
网络搜索和学术搜索：
Enter the search term in the input box
Click the "搜索" (Search) or "学术" (Academic Search) button to perform the search
The search results will be displayed in the browser
Notes
Make sure you have the necessary API keys for the AI services if you want to use the AI chat functions. Follow the instructions in the code to configure the API keys.
Keep your API keys secure and do not share them with others.
The application requires an internet connection for some functions such as web search, image download, and AI chat.
Use the application in accordance with the laws and regulations and ethical standards.
Contact
If you have any questions or issues regarding the application, please contact the author at 84406570@qq.com.

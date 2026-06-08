# Day 1: AI Concepts

## Contents

- [1. Purpose](#1-purpose)
- [2. Setup](#2-setup)
  - [2.1 Get a Groq API key](#21-get-a-groq-api-key)
  - [2.2 Download Open WebUI Desktop](#22-download-open-webui-desktop)
  - [2.3 Launch and first-time setup](#23-launch-and-first-time-setup)

## 1. Purpose

Students will become familiar with the following concepts of modern AI usage:

- Local and hybrid-hosted models
- Skills
- MCPs
- Loops

## 2. Setup

### 2.1 Get a Groq API key

Open WebUI will use [Groq](https://groq.com/) to run cloud-hosted models. Groq offers a free tier and does not require a credit card.

1. Go to the [Groq Console](https://console.groq.com/) and sign up with email, Google, or GitHub.
2. Verify your email if prompted.
3. Open [**API Keys**](https://console.groq.com/keys) in the left sidebar.
4. Click **Create API Key**, give it a name (for example, `open-webui`), and click **Submit**.
5. Copy the key immediately. It starts with `gsk_` and is only shown once. If you lose it, create a new key.

Keep the key somewhere safe for the next section. You will paste it into Open WebUI in step 6 of [§2.3](#23-launch-and-first-time-setup).

> Do not commit your API key to git or share it publicly.

> **Warning:** Groq's free tier provides enough tokens to get you through this class, but it has daily rate limits. Stick to the course outline—avoid extra experimentation or unrelated prompts, or you may hit your limit before the course is over.

### 2.2 Download Open WebUI Desktop

Go to the [Open WebUI Desktop download page](https://github.com/open-webui/desktop#download) and install the build for your platform.

### 2.3 Launch and first-time setup

1. Open **Open WebUI** from your applications menu or Start menu.
2. Select the option to **Run Locally**.
3. Select the **Open WebUI** connection on the left and create a local admin account:

| ![image01.png](../imgs/image01.png) |
|:--:|
| _Create a local admin account_ |

4. You should now see the chat input area:

| ![image02.png](../imgs/image02.png) |
|:--:|
| _Verify Open WebUI_ |

5. Open **Settings** by clicking your profile icon → **Settings**:

| ![image03.png](../imgs/image03.png) |
|:--:|
| _Open settings_ |

6. Under **OpenAI API** → **Manage OpenAI API Connections**, click the **+** button.

   - Set URL to:

     ```text
     https://api.groq.com/openai/v1
     ```

   - Under **Auth**, select **Bearer**
   - Paste your Groq API key
   - Press **Save**

| ![image04.png](../imgs/image04.png) |
|:--:|
| _Configure Groq connection_ |

7. Press **New Chat**. You should now see a dropdown of models in the upper-left corner:

   - Select **`llama-3.1-8b-instant`**

| ![image05.png](../imgs/image05.png) |
|:--:|
| _Validate models appear_ |

8. Send a test prompt and verify the model responds:

| ![image06.png](../imgs/image06.png) |
|:--:|
| _Test model response_ |

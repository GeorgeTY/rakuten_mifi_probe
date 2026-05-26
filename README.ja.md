# Rakuten MiFi Signal Probe (日本語版)

[English Edition](README.md)

本ツールは、**楽天モバイル（Rakuten Mobile）の4G MiFiルーター**（Rakuten WiFi Pocket Platinumなど）向けに、電波強度メトリクスとリアルタイムのネットワーク速度をターミナル上に表示する、依存関係なしの軽量なPythonスクリプトです。

PCやNAS、Raspberry Pi、自宅のサーバーなどの端末から直接実行できるため、モバイルルーターを室内のどこに設置すれば最も電波をキャッチしやすいか（最適な設置場所）を探すのに役立ちます。

---

> [!IMPORTANT]
> **検証済みデバイス**: 本スクリプトは **Rakuten WiFi Pocket Platinum (4G)** でのみ動作検証を行っています。
> **使用目的**: このスクリプトは、ユーザーが物理的な設置場所を調整し、より良いセルラー電波を受信しやすくするための利便性の向上のみを目的としています。

---

## 主な機能

- **リアルタイムポーリング**: 信号パラメータとトラフィック速度を1秒ごとに取得・更新します。
- **表示される主なメトリクス**:
  - **RSRP**（基準信号受信電力、単位: dBm）
  - **RSRQ**（基準信号受信品質、単位: dB）
  - **SNR**（信号対雑音比、単位: dB）
  - **アップロード（Upload ↑）** および **ダウンロード（Download ↓）** のリアルタイム速度（KiB/s または MiB/s 表示）
- **依存関係なし (Zero Dependencies)**: Pythonの標準ライブラリ（`urllib` と `json`）のみで構築されているため、`pip`などによる外部ライブラリのインストールは一切不要です。
- **対話型セットアップウィザード**: 初回起動時に接続設定やログイン情報を入力するための対話画面が自動で立ち上がり、安全に `config.json` を生成します。
- **安全設計 (Git-Safe)**: ルーターのログインパスワードが含まれる `config.json` は、Gitの追跡対象から自動的に除外されるため、誤ってGitHubなどの公開リポジトリにパスワードが流出する心配はありません。

---

## インストールと準備

1. 本プロジェクトのフォルダ全体を、任意の作業ディレクトリにコピーまたはクローンします。
2. **Python 3** がインストールされていることを確認します：
   ```bash
   python3 --version
   ```

---

## 使い方

ターミナルでスクリプトを実行するだけです：

```bash
python3 probe.py
```

### 初回起動時の対話型セットアップ
ディレクトリ内に `config.json` が見つからない場合、セットアップウィザードが自動的に開始されます。以下の項目を入力してください：
- **Router IP Address**（ルーターのIPアドレス、デフォルト: `192.168.0.1`）
- **Admin Username**（管理ユーザー名、デフォルト: `admin`）
- **Admin Password**（ルーターのWeb管理画面用のパスワード）

入力が完了すると、自動的に `config.json` が生成され、電波強度の監視がスタートします。

### 手動での設定
スクリプトを実行する前に、手動で `config.json` を作成することも可能です。`config.example.json` を参考にして、以下のフォーマットで保存してください：

```json
{
  "router_ip": "192.168.0.1",
  "username": "admin",
  "password": "YOUR_ROUTER_PASSWORD"
}
```

---

## ターミナル出力例

実行が成功すると、ターミナル上に以下のようなリアルタイムのログが表示されます：

```text
[*] Connecting to router at http://192.168.0.1...
[*] Authenticating...
[+] Login successful!
[*] Polling signal parameters... (Press Ctrl+C to exit)
----------------------------------------------------------------------------------------
RSRP:  -92 dBm  |  RSRQ:  -14 dB  |  SNR:   0.0 dB  |  Upload ↑:   4.63 KiB/s  |  Download ↓:   7.02 KiB/s
RSRP:  -92 dBm  |  RSRQ:  -14 dB  |  SNR:   0.0 dB  |  Upload ↑:   1.53 KiB/s  |  Download ↓:   3.12 KiB/s
RSRP:  -92 dBm  |  RSRQ:  -14 dB  |  SNR:  -0.8 dB  |  Upload ↑:   1.53 KiB/s  |  Download ↓:   3.12 KiB/s
RSRP:  -92 dBm  |  RSRQ:  -14 dB  |  SNR:  -0.8 dB  |  Upload ↑:   3.66 KiB/s  |  Download ↓:   1.10 KiB/s
```

終了するには、いつでも `Ctrl + C` を押してください。

---

## ライセンスと免責事項

本プロジェクトは [MIT License](LICENSE) の下でライセンスされています。

**免責事項**: 本プロジェクトは個人によって作成された非公式のコミュニティツールです。楽天モバイル株式会社、またはハードウェアの製造メーカー等とは一切関係ありません。本ツールは **Rakuten WiFi Pocket Platinum (4G)** でのみ検証されており、最適な信号位置を特定することのみを目的に設計されています。本ツールの使用によって生じたあらゆるトラブルや不利益について、作者は一切の責任を負いません。自己責任においてご使用ください。

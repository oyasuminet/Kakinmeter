# Kakinmeter — Bionic+ 週間使用量ウィジェット（Rainmeter）

Bionic+ の**週間クラウド使用量**（残り/上限・バー・リセットまでのカウントダウン）を
アプリを開かずにデスクトップに表示する Rainmeter スキンです。

データは Bionic のローカルアカウントキャッシュから読みます：

```
%USERPROFILE%\.lmstudio\apps\bionic\.internal\cloud-account.json
```

> ⚠️ このファイルには `ownerKey` などアカウント秘密情報が含まれます。
> 本ウィジェットは**使用量フィールドのみ**を読み、それ以外を表示・記録しません。
> ファイル自体を共有しないでください。

## 内容物

| ファイル | 役割 |
| --- | --- |
| `Bionic_cloud.py` | 上記 JSON を読み `cloud_status.txt`（ASCII `key=value`）を自身の横に書き出す |
| `Kakinmeter.ini` | Rainmeter スキン本体 |
| `cloud_status.txt` | 出力（初回実行時に自動生成） |

## セットアップ

1. [Rainmeter](https://www.rainmeter.net/) を導入し、このフォルダを
   `%USERPROFILE%\AppData\Roaming\Rainmeter\Skins\` にコピー。
2. `Bionic_cloud.py` を定期実行するタスクを登録（**pythonw.exe**＝ウィンドウなし）。
   Windows タスクスケジューラの場合：
   - プログラム: `<Python導入先>\pythonw.exe`
   - 引数: `"%USERPROFILE%\AppData\Roaming\Rainmeter\Skins\Kakinmeter\Bionic_cloud.py"`
   - トリガー: ログオン時・1分間隔で繰り返し・期限なし
   - 他のスケジューラでも可（小さなテキストを書き出すだけです）
3. Rainmeter のタスクトレイアイコン右クリック → **すべて再読み込み** →
   スキン `Kakinmeter\Kakinmeter` を読み込み。

### パスの変更

- スクリプトは既定で**自分と同じフォルダ**に `cloud_status.txt` を書き出します。
  スキンフォルダを別場所に置く場合は第2引数で出力先を指定できます：
  `pythonw.exe Bionic_cloud.py "<account.jsonのパス>" "<cloud_status.txtのパス>"`
- `Kakinmeter.ini` の `STATUS_FILE` は `#CURRENTPATH#`（スキンフォルダ内）を指すため、
  スキンとしてインストールすれば既定のままで揃います。

## タイムゾーンについて

リセット日時の表示は **お使いの PC のローカル時刻**です（Bionic の `resetsAtIso`＝UTC を
ローカルに変換して表示）。値が取得できない/過去の場合のフォールバックは、実測された
リセット スケジュール「**毎週月曜 00:00 UTC**」を計算に使います。地域の固定値はありません。

## バーの色

- 紫： 通常
- 赤： 残り 20% 以下

## 文字コードの注意

- リポジトリの `Kakinmeter.ini` は ASCII（英語UI）です。Rainmeter は ANSI/ASCII の .ini を
  直接読めます。**日本語など非ASCII文字を入れる場合は UTF-16LE（BOMあり）・CRLF で再保存**。
- `cloud_status.txt` の出力は 100% ASCII です。

## ライセンス

個人利用向け。無保証。

© oyasuminet + Bionic ローカルLLMエージェント + GoogleSearch_AI


# Gitlab runnerに関して

Gitlab runnnerとCICDに関するメモです。

## Gitlab runnerとは、何ができるの？
[詳しくはこちらを参照](https://docs.gitlab.com/runner/)  
Gitlabと連携して自動テスト、自動デプロイなどを実行可能なアプライアンス、ミドルウェア（？）  
いわゆるCICDを行うことができる

CLI(だいたいはシェル？)から実行できるものについては基本的に実行可能（ただし操作によっては事前に環境を整えておく必要あり。ツールのインストール、実行権限の割り当てなど）

- リポジトリのコードを引っ張ってくる。
- 作成したシェルをコマンドで叩くように設定すれば複雑な処理も実行可能

- 実行を行うことで作成されたファイル(サマリーやログファイル)をGitLabのGUIからダウンロード可能。

- 利用ケースとしてはコードのビルド、コードのテスト(構文テスト、E2Eテスト、ドライラン的なことも実行可能)、コードのデプロイなどで使われることが多い。

- 発想を膨らませればもっと色々なことができそう。。

## Gitlab runnerについて詳しく、インストール方法など

Gitlab自体がインストールされたものと別のVMにインストールする。  
インストールの形態としては以下の通り  
- VM(Debian,Ubuntu,REHL,Cent,Windows)
- Dockerコンテナ
- k8s(エージェント、オペレーター)→現状調べられていない。  

利用可能まで以下２ステップ
1. Runner自体のインストール(Linuxの場合、数ステップだけとっても簡単)
2. リポジトリへRunnerの登録。(Runner側でGitlab自体のFQDNとリポジトリのTokenを入力することで登録可能)

[手順はこちらを参考](https://docs.gitlab.com/14.10/runner/install/)

## 実行環境、実行方法に関して
RunnerをGitlabへ登録する際、実行形態(Executer)を選択。Runnerごとに１つ選択する。
- shell(Runnerのシェル上で実行、環境は汚れやすい)
- docker(コンテナイメージを設定し、コンテナを作成して実行)
- SSH(sshでコマンドを投げるだけ)
- k8s(Podを作成して実行)

リポジトリのルートフォルダーに存在する.gitlab-ci.ymlに書かれた内容を上記実行形態で実行する。  
以下のタイミングの中から選択して、実行される。(.gitlab-ci.ymlに記載する)
- プッシュ時
- マージ時
- スケジュールで指定された時間
- Gitlab UIのボタンが押された時(CDのときはこちらを使用してもいいかも)

特定のブランチに限定したり特定のブランチを除くことも可能。
処理に失敗したらマージ、プッシュなどはされない。

## サンプル


 .gitlab-ci.ymlのサンプル
```yaml
# キャッシュの保存先
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

# pip installしたものをキャッシュするためにvirtualenvを導入
cache:
  paths:
    - .cache/pip
    - venv/

# 実行前スクリプト
before_script:
  - python3 -V
  - virtualenv venv
  - source venv/bin/activate

# testというstageを使う
test:
  script:
    # - python setup.py test
    - pip install flake8
    - flake8 *.py --exclude venv/,.cache --ignore E501
  only:
    refs:
      - merge_requests
```
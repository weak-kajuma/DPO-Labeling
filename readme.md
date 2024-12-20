# DPO Labeling
このプログラムはDPOやRLHFのラベリングのために作成されました。

## How to use
```sh
git clone https://github.com/weak-kajuma/DPO-Labeling
python3.11 -m venv .venv
source .venv/bin/activate

pip install customtkinter
python main.py
```
起動しましたら、Load JSONを押してjsonファイルを読み込んでください。  
矢印ボタン左右でデータ間の移動、  
矢印ボタン上下でfeedback\(good/bad\)の付与、  
Save JSONでjsonファイルの保存です。  
適度に保存してください。データが失われます。

### Args
- \-i \-\-input input.json: 入力のprompt-answerペアのjsonファイル名
```json:input.json
[
    {
        "prompt": "仕事の熱意を取り戻すためのアイデアを5つ挙げてください。",
        "answer": "1. 自分の仕事に対する興味を再発見するために、新しい技能や知識を学ぶこと。 2. カレッジやセミナーなどで講演を聴くことで、仕事に対する新しいアイデアや視点を得ること。 3. 仕事に対してストレスを感じている場合は、ストレスマネジメントのテクニックを学ぶこと。 4. 仕事以外の楽しいことをすることで、ストレスを発散すること。 5. 仕事に対して自己評価をすることで、自分がどのように進化しているのかを知ること。"
    },
    {
        "prompt": "クマが海辺に行ってアザラシと友達になり、最終的には家に帰るというプロットの短編小説を書いてください。",
        "answer": "クマは、森での生活に飽き飽きし、新しい冒険を求めて海辺に向かった。彼は海に興味があり、そこに住む生き物たちと出会いたかった。彼は旅をするために必要なものを準備し海辺へと向かった。 海辺に到着したクマは、アザラシたちと出会った。彼らはクマを受け入れてくれ、一緒に遊んだり、話をしたりするようになった。クマはアザラシたちとの楽しい時間を過ごし、彼らとの友情を育んでいった。 だが、クマは家族の元に帰らなければならなかった。彼はアザラシたちに別れを告げなければならなかった。しかし、彼は彼らとの楽しい時間を思い出し、彼らとの友情を大切にしたくて、家に帰ることができなかった。彼は葛藤しながらも、最終的にはアザラシたちに別れを告げ、家に帰った。だが、それでも彼はアザラシたちとの思い出を胸にして、永遠に忘れない。"
    }
]
```

- \-o \-\-output output.json: 出力のjsonファイル名
```json:input.json
[
    {
        "prompt": "仕事の熱意を取り戻すためのアイデアを5つ挙げてください。",
        "answer": "1. 自分の仕事に対する興味を再発見するために、新しい技能や知識を学ぶこと。 2. カレッジやセミナーなどで講演を聴くことで、仕事に対する新しいアイデアや視点を得ること。 3. 仕事に対してストレスを感じている場合は、ストレスマネジメントのテクニックを学ぶこと。 4. 仕事以外の楽しいことをすることで、ストレスを発散すること。 5. 仕事に対して自己評価をすることで、自分がどのように進化しているのかを知ること。",
        "feedback": "good"
    },
    {
        "prompt": "クマが海辺に行ってアザラシと友達になり、最終的には家に帰るというプロットの短編小説を書いてください。",
        "answer": "クマは、森での生活に飽き飽きし、新しい冒険を求めて海辺に向かった。彼は海に興味があり、そこに住む生き物たちと出会いたかった。彼は旅をするために必要なものを準備し海辺へと向かった。 海辺に到着したクマは、アザラシたちと出会った。彼らはクマを受け入れてくれ、一緒に遊んだり、話をしたりするようになった。クマはアザラシたちとの楽しい時間を過ごし、彼らとの友情を育んでいった。 だが、クマは家族の元に帰らなければならなかった。彼はアザラシたちに別れを告げなければならなかった。しかし、彼は彼らとの楽しい時間を思い出し、彼らとの友情を大切にしたくて、家に帰ることができなかった。彼は葛藤しながらも、最終的にはアザラシたちに別れを告げ、家に帰った。だが、それでも彼はアザラシたちとの思い出を胸にして、永遠に忘れない。",
        "feedback": "bad"
    }
]
```

## 参考
- [サブモニターで表示する用の、簡単なmdメモ閲覧GUIアプリをpythonのCustomTkinterで作成した。](https://qiita.com/RamuRaito/items/93fd7d8a060afc82b8bc)
- [elyza/ELYZA-tasks-100](https://huggingface.co/datasets/elyza/ELYZA-tasks-100?row=1)

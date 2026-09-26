## 发出拉取请求

好，你已经从团队那里获得认可，确认你的改动是好的，也实现了当初设定的设计。那么，**实际发出**拉取请求最有效的方式是什么？你为这些改动辛苦了很久，希望团队其他成员重视你的拉取请求并快速给出反馈。该怎么做？

还记得前面说过，代码评审最重要的部分是保持团队集体心智模型良好对齐吗？你的同事很可能正在忙完全不同的东西，也许在系统的完全不同的部位。他们的大脑处在完全不同的上下文里，所以你必须克服这一点——给他们提供完成评审所需的、有帮助的引导。这意味着要写一份条理清晰的说明：你做了哪些改动、为什么这么做，以及他们只读代码得不到的其它相关信息。别让同事做超出必要的脑力劳动。

我们来看几个拉取请求说明的好例子与坏例子：

坏例子：

```
Title: Fix uninitialized memory bug
Description:

This is the bug Bob and I talked about earlier. I had
trouble with the compiler but managed to make this work. Let me
know what you guys think.
```

如果你是这位拉取请求的作者，请停下来，先把自己放到代码评审者的位置上想一秒。标题含糊，引发的问题比给出的答案还多：内存 bug 在哪？这个改动有多关键？你和 Bob 之前聊的是哪个 bug？你在编译器上遇到了什么麻烦？描述里既没有提供关于问题的有用上下文，也没有对改动的有用说明。如果这个拉取请求很长，评审者就得先扎进代码里、做一番脑力体操来拼凑上下文，才谈得上思考这个改动在整个系统设计中的位置。

下面是一个改进版，它让改动集清楚多了：

```
Title: Fix process crash on startup from uninitialized memory [#54633]
Description:

This bug was causing process crashes on boot due to a memory
initialization error in our statistics Counter class. I talked this
over with Bob, and we both agree the crashes are a rare edge case
that don't warrant a hot-fix release. Here's a summary of the
changes:

  - Moved the underlying int variable into the class initializer
    to prevent ununitialized memory in the Counter.
  - Reworked the Counter interface to simplify caller conditional
    logic and prevent further off-by-one counting problems.
  - Added a unit test that exposes the crash

Testing: I've verified the test suite still passes, and verified
manually that the crash doesn't happen locally.
```

这份拉取请求说明在几处有所改进：标题足够有描述性，能让评审者获得一点简短上下文，并吸引他们点开邮件了解更多。评审者知道这是进程崩溃（通常是相当糟糕的事），而且还有一个 bug 报告编号，如果他想更深入了解这个问题，可以去读该 bug 报告的更多细节。新的描述还指出了问题出在哪里，有助于提供关于这个修复有多关键的上下文。其中有一段摘要列出了拉取请求中高层面的结构性改动，让评审者在看代码之前就先在脑中形成图景。**代码评审者不应该被看到的东西惊到。** 这个例子还说明了做过哪些测试，让评审者确信这些改动经过深思、测试充分、可以合并了。把「点击合并」这件事做得傻瓜式简单，就是为评审者的成功铺路。

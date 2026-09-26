## 什么是 SAST？

静态应用安全测试（SAST）是一种[白盒](https://en.wikipedia.org/wiki/White-box_testing)安全测试方法。SAST [利用应用的静态源代码](/en_us/blog/learn/static-code-analysis.html)或二进制文件来识别漏洞。也就是说，SAST 工具在应用**未运行**的状态下对代码进行分析。

开发者用 SAST 检测各类安全风险，例如代码中的[跨站脚本攻击（XSS）](/en_us/blog/learn/cross-site-scripting-xss-attacks.html)、不安全的反序列化、缓冲区溢出，以及[其它 OWASP 漏洞](/en_us/blog/learn/owasp-top-10.html)。由于单靠 SAST 无法识别运行时特有的漏洞，开发者常常必须把 SAST 与其它测试方法结合起来，才能实现全面的安全。

SAST 是[软件开发生命周期](/en_us/blog/learn/software-development-lifecycle-sdlc.html)的重要组成部分，因为它能**尽早**发现漏洞。越早发现，修复成本越低。由于 SAST 工具可以在开发阶段执行，开发者如今能在产品发布上市之前，对代码编写并测试**上千次**（！！）。

SAST 可以集成进 [CI/CD 管线](/en_us/blog/learn/ci-cd-devops-pipeline.html)，这样做时它被称为「安全 DevOps」或「[DevSecOps](/en_us/blog/learn/devsecops-concepts-principles.html)」。SAST 借助自动化具备良好的可扩展性。能够把覆盖 SAST 技术的自动化测试落地，使它成为快速应对代码层风险的高效方案。

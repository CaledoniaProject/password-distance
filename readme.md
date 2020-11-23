## 说明

解析 [philipperemy/tensorflow-1.4-billion-password-analysis](https://github.com/philipperemy/tensorflow-1.4-billion-password-analysis) 执行结果，并不断排除已知的变形方式，最终形成一套密码变形规则。

已知类型:

* Winnie1 -> winnie1
* 12345y -> 12345Y
* crazymom -> crazymom1
* spiderman -> 1spiderman
* 1997narek1997 -> 1997Narek1997
* m12345 -> 12345m
* xaiver4 -> xaiver5

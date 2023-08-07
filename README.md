# 安装教程

```
    conda create --name paddle python=3.7
    conda activate paddle
    python -m pip install paddlepaddle-gpu==2.4.2.post117 -f https://www.paddlepaddle.org.cn/whl/windows/mkl/avx/stable.html
    git clone https://gitee.com/paddlepaddle/PaddleClas.git
    cd PaddleClas
    pip install -r requirements.txt
```
经过详细分析，我完全理解了问题所在。当前的 setup.bat 文件确实与 setup.sh 存在显著功能差距，主要问题包括：
缺少原生安装选项：setup.sh 支持 Docker 和 Native 两种安装方式，而 setup.bat 只实现了 Docker 安装
菜单误导性：虽然菜单显示"Both options provide the same functionality!"，但实际上只实现了选项1
帮助文档不一致：帮助信息中提到了 --native 选项，但代码中没有实现
功能缺失：缺少 Python 环境检查、PDM 包管理器安装、虚拟环境创建、依赖包安装等原生环境支持功能
让我来增强 setup.bat 文件，使其功能与 setup.sh 保持一致。
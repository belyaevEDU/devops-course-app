# Итоговый проект с курса DevOps от YADRO
⚠️ репозиторий был перенесен из GitLab, как следствие референсы на MRы в сообщениях коммитов будут вести на несвязанные с ними PRы в этом репозитории ⚠️

⚠️ из-за ресурсных лимитаций во время собственных доработок, у меня не было полноценного dev окружения, поэтому история main ветки несколько грязная (как и история helm репозитория...) ⚠️
## Репозитории, связанные с проектом
https://github.com/belyaevEDU/devops-app-helm - Helm для развертывания приложения + observability stack values

https://github.com/belyaevEDU/repeating-functions-sharedlib - shared library для Jenkins пайплайна, содержит функцию для ожидания поднятия приложения.

## Общие сведения

Проект заключался в:
- написании [простого API на Python и FastAPI](/app/README.md)
- развертывании Kubernetes кластера на трех виртуальных машинах с помощью Ansible
- построении CI/CD процесса, который бы проводил линтинг, сборку образа, тестировал и развертывал приложение на Kubernetes кластере

Далее проект был перенесен с Yadro's GitLab и их инфраструктуры на GitHub и собственную инф-ру для доработки. Список доработок:
- Перенос CNI и Ingress controller с Calico + ingress-nginx на Cilium ([#9](https://github.com/belyaevEDU/devops-course-app/issues/9))
- Мониторинг с Grafana, Prometheus, Grafana Loki & Alloy. К тому же, приложение было инструментировано для Prometheus ([#12](https://github.com/belyaevEDU/devops-course-app/issues/12))

## Построенный процесс и используемые технологии

### CI процесс

![](/docs/ci.png)

При отправке изменений в репозиторий, хост репозитория отправляет сообщение вебхуку Jenkins. Запускается пайплайн, описанный в [Jenkinsfile](/Jenkinsfile) и схематично представленный на диаграмме. В диаграмме пайплайна, первый блок - триггер, далее сами шаги.

В CI пайплайне были использованы следующие инструменты для своих согласных шагов:
- Lint - линтинг исходного кода приложения на Python: Ruff
- SAST - статическое тестирование безопасности с правилами, согласно используемым в приложении технологиям: Semgrep
- Build: [Docker](/Dockerfile)
- Test: [Docker](/Dockerfile) с [hardened docker-compose файлом](/docker-compose.yml) + Newman [с тестами для Postman](/testing/postman_tests.json)
- SCA: Trivy
- Publish: Docker, образ отправляется на Docker Hub

### CD процесс

![](/docs/cd.png)

В основе процесса continuous deployment взята методология GitOps.

Приложение развернуто с помощью [ArgoCD](/k8s/argocd/application), [ArgoCD Image Updater](/k8s/argocd/imageupdater/) и Helm.

На GitHub был создан отдельный [репозиторий](https://github.com/belyaevEDU/devops-app-helm), на котором лежит Helm chart для развертывания приложения в staging-окружении и production-окружении.

CI, при триггере тэга или master, заканчивается шагом "Publish" *(не считая cleanup)*, который публикует новый образ в Docker Hub. Если Image Updater видит новую версию приложения, то он обновляет в Helm репозитории values файлы, меняя именно версию. ArgoCD же по webhook получает уведомления о изменениях в Helm репозитории и обновляет те приложения, которые получили изменения.

## Observability

Эта часть - доработка после завершения курса с целью освоить этот ряд технологий.

В Kubernetes кластере был развернут kube-prometheus-stack, Grafana Loki и Alloy.

К тому же, приложение было инструментировано под Prometheus с помощью модуля [prometheus-fastapi-instrumentator](https://pypi.org/project/prometheus-fastapi-instrumentator/), который отдает метрики по ручке */metrics*. Для этого приложение запускает отдельный HTTP сервер на порте 9100, который не выводится Ingress.

Kube-prometheus-stack включает в себя Grafana и Prometheus.

![](/docs/logging.png)

В helm чарте приложения появился ServiceMonitor, который собирает метрики от приложения по ручке */metrics* каждые 30 секунд. К тому же, был добавлен лейбл, по которому Alloy собирает логи приложения.

## Получение трафика из открытой сети

Нам выделенная инфраструктура от Yadro на время курса и моя локальная стоит за CGNAT. Как следствие, для получения трафика из открытой сети требуется reverse proxy. Для этого был использован проект [frp](https://github.com/fatedier/frp). Манифесты для деплоймента frp client находятся [здесь](/k8s/frpc/).

И трафик идет следующим образом:

![](/docs/traffic.png)

К тому же, в диаграмме неймспейса currency в секции Observability можно заметить cert-issuer, который запрашивает TLS сертификат от LetsEncrypt для возможности запросов с HTTPS.

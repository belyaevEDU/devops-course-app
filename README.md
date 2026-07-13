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

CI процесс выглядит следующим образом:

![](/docs/ci_process.png)

При отправке изменений в репозиторий, хост репозитория отправляет сообщение вебхуку Jenkins. Запускается пайплайн, описанный в [Jenkinsfile](/Jenkinsfile) и схематично представленный на диаграмме. В диаграмме пайплайна, первый блок - триггер, далее сами шаги.

В CI пайплайне были использованы следующие инструменты для своих согласных шагов:
- Lint - линтинг исходного кода приложения на Python: Ruff
- SAST - статическое тестирование безопасности с правилами, согласно используемым в приложении технологиям: Semgrep
- Build: [Docker](/Dockerfile)
- Test: [Docker](/Dockerfile) с [hardened docker-compose файлом](/docker-compose.yml) + Newman [с тестами для Postman](/testing/postman_tests.json)
- SCA: Trivy
- Publish: Docker, образ отправляется на Dockerhub


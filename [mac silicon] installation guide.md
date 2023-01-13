### 들어가며

이 글은 Apple silicon 환경에서 minikube를 활용해 로컬로 kubeflow 구축하는 방법을 설명합니다. kubeflow 설치를 위한 여러 종류의 가이드가 있었지만 Apple silicon에서는 특정 단계에서 arm64 호환 문제로인해 설치가 불가능했습니다.

Apple silicon 기반에서 설치 가이드를 따라하기 힘든 이유는 주로 가상환경을 지원하는 프로그램이 Arm64를 호환하지 않는 경우와 kubeflow 일부 컴포넌트가 Arm64를 호환하지 않는 경우 때문입니다. 다양한 시도를 통해 알아낸 바로는 Apple slilcon 기반의 로컬에서 kubeflow를 설치하기 위해선 Docker를 통해 kubernetes를 실행하고, kubeflow 1.6 버전을 설치 해야합니다.

kubeflow를 설치하고 운영하는 것이 목적이 아닌, kubeflow 사용이 주 목적이라면 클라우드 환경에서 kubeflow를 지원하는 Arrikto를 활용하는 것을 권장합니다. [Arrikto 페이지](https://www.arrikto.com/kubeflow-as-a-service/)

### 주의사항

- kubeflow를 설치하는 과정이 매끄럽지만은 않습니다. 아래 설명대로 설치하지 않는 이상 제대로 설치되지 않을 가능성이 높습니다.
- 에러 원인을 파악하는 단계에서 많은 시간 소모가 발생할 수 있으니 최대한 설명대로 따라해주세요.

### 기존 설치한 프로그램 제거

kubflow는 다음의 환경에서만 실행 가능합니다. 버전을 맞추기 위해 기존 프로그램들을 제거한 뒤 새롭게 설치하겠습니다.

```
- kubernetes 1.21.
- kustomize 3.2.0
- kubectl 1.21.
```

기존에 설치한 프로그램을 먼저 제거하겠습니다.

```
$ brew uninstall minikube
$ brew uninstall kubectl
$ brew uninstall kustomize
$ brew cleanup
```

- 기존 설치된 프로그램 제거
  - minikube
  - kubectl
  - kustomize
  - brew cleanup

### colima 설치(권장사항)

colima는 docker desktop 사용 없이 docker 사용을 가능하게 만드는 프로그램입니다. brew를 통해 간단하게 설치할 수 있고 사용법 또한 간단합니다. colima를 사용하지 않아도 docker desktop을 활용해 설치가이드를 따라 할 수 있습니다.

colima 설치에 다소 시간이 소요됩니다.

```
$ brew install colima

$ colima version
```

### kustomize 3.2.0 설치

지웠던 프로그램들을 버전에 맞게 재설치 하겠습니다. 설치 순서는 kustomize => kubectl => minkube 순 입니다. brew는 최신 버전만 지원하므로 bin으로 kustomize 3.2.0을 설치하겠습니다.

```
$ brew install wget
$ wget https://github.com/kubernetes-sigs/kustomize/releases/download/v3.2.0/kustomize_3.2.0_darwin_amd64
$ chmod +x kustomize_3.2.0_darwin_amd64
$ mv kustomize_3.2.0_darwin_amd64 /usr/local/bin/kustomize
$ export PATH=$PATH:/usr/local/bin/kustomize
```

```
$ kustomize version

>>> Version: {KustomizeVersion:3.2.0 GitCommit:a3103f1e62ddb5b696daa3fd359bb6f2e8333b49 BuildDate:2019-09-18T16:26:36Z GoOs:darwin GoArch:amd64}
```

### kubectl 1.21.12 설치

```
$ curl -LO "https://dl.k8s.io/release/v1.21.12/bin/darwin/arm64/kubectl"
$ chmod +x ./kubectl
$ sudo mv ./kubectl /usr/local/bin/kubectl
$ sudo chown root: /usr/local/bin/kubectl
```

### minikube 설치

```
brew install minikube
```

### kubeflow 1.6 로컬에 저장

kubeflow 1.6은 Istio 1.16 버전을 지원합니다. Istio는 1.16 버전부터 Arm64를 지원하므로 Apple silicon 환경에서는 kubeflow 1.6을 설치해야합니다.

Apple silicon 환경에서 kubeflow 1.6 보다 낮은 버전을 설치하게 되면 Istio의 호환 때문에 사용할 수 없습니다. pods 상태에서 Istio의 상태가 pending으로 유지되기 때문입니다.

kubeflow 1.6을 로컬에 저장하겠습니다.

```
git clone https://github.com/kubeflow/manifests.git

cd manifests
```

### minikube 실행

본격적으로 kubeflow를 설치하겠습니다. 먼저 docker 환경에서 minikube를 실행하겠습니다. colima를 사용하는 경우 `colima start --cpu 4 --memory 9`를 docker를 사용하는 경우 `docker desktop`을 실행해주세요.

docker기반으로 minikube를 실행해야 하므로 driver를 docker로 설정하고 kubernetes 1.21.12 버전을 설정합니다.

```
$ minikube start --driver=docker --kubernetes-version=1.21.12 --memory=8192 cpus=4
```

memory, cpu가 정상적으로 할당 됐는지 확인

```
$ minikube config view vm-driver
```

### kubeflow 설치

kubeflow는 수십개의 컴포넌트로 구성되어 있습니다. 개별 컴포넌트들이 실행되고 연결되면서 kubeflow를 이루게 됩니다. kubeflow가 개별 component별로 구성된 만큼 목적에 맞게 필요한 컴포넌트만 불러올 수 있습니다. [kubeflow github](https://github.com/kubeflow/manifests)에는 컴포넌트별로 불러오는 방법을 소개하고 있습니다.

kubeflow를 구성하는 컴포넌트 전부를 불러오는 명령어는 다음과 같습니다. 모든 컴포넌트가 불러와질 때 까지 10초 간격으로 반복하는 명령어입니다. 평균 3회의 루프를 진행하면 모든 컴포넌트들이 불러와집니다. 컴포넌트를 불러온 다음 실제 실행되기 까지는 10~30분 정도 소요됩니다.

```
while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done
```

> **!주의** 무한루프에 빠졌다면 10분 정도 내버려 둔 뒤 `control(^)+C`를 눌러 종료해주세요.

무한루프를 경험하지 않은 경우 다음 과정으로 넘어가세요.

개인적인 경우로 1.6 버전 설치 시 무한루프를 경험했습니다. 1.5 버전 설치 시에는 경험하지 못했습니다. 아마 `Profiles + KFAM` 컴포넌트가 제대로 불러와지지 않아 발생한 것 같습니다.

```
error: resource mapping not found for name: "kubeflow-user-example-com" namespace: "" from "STDIN": no matches for kind "Profile" in version "kubeflow.org/v1beta1"
ensure CRDs are installed first
```

이러한 에러가 발생했고 루프 종료 후 namespace에 `kubeflow-user-example-com`만 등록되지 않았습니다. `Profiles + KFAM`가 설치되지 않으니 `kubeflow-user-example-com`에 필요한 조건이 형성되지 않아 발생한 것 같습니다. 실제로 아래의 명령어를 실행해 `Profiles + KFAM`와 `kubeflow-user-example-com`를 설치하니 정상 작동했습니다.

명령어 실행에 앞서 다른 컴포넌트가 정상적으로 불러와졌는지 확인해야합니다. 10분 간 루프 상태로 내버려 두게 되면 거의 모든 컴포넌트 상태가 running으로 나타나 있습니다. Training operator의 경우 crashloopbackoff 또는 Error 상태가 되도 무방합니다. 다음 단계에서 설명할 내용입니다.

```
# 컴포넌트가 정상작동하는지 확인

kubectl get pods --all-namespaces
```

Training operator를 제외한 모든 컴포넌트가 running 상태라면 아래의 명령어를 실행하세요.

```
kustomize build apps/profiles/upstream/overlays/kubeflow | kubectl apply -f -

kustomize build common/user-namespace/base | kubectl apply -f -
```

### Training operator 재설치

개인적인 경험으로 Training operator는 kubeflow 버전을 망라하고 설치가 되지 않았습니다. Training operator 상태가 crashloopbackoff 또는 Error 인 경우 아래 명령어를 실행해 주세요. 상태가 OOMKilled인 경우 메모리가 부족해서 실행되지 않는 것이므로 메모리 크기를 늘려주세요.

```
kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone"
```

### 최종상태 점점

최종적으로 namespace 별로 컴포넌트가 제대로 실행됐는지 하나하나 확인해 봅시다. 혹여나 제대로 실행되지 않았거나 존재하지 않은 경우 [kubeflow github](https://github.com/kubeflow/manifests)를 참고해 실행해주세요.

```bash
$ kubectl get pods -n cert-manager
$ kubectl get pods -n istio-system
$ kubectl get pods -n knative-eventing
$ kubectl get pods -n auth
$ kubectl get pods -n knative-serving
$ kubectl get pods -n kubeflow
$ kubectl get pods -n kubeflow-user-example-com
```

### kubeflow 실행하기

아래 명령어를 실행한 뒤 [localhost:8080](http://localhost:8080)에 접속하세요.

```bash

kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80

```

아이디와 비밀번호를 입력하면 kubeflow에 접속합니다.

- Email Address: `user@example.com`
- Password: `12341234`

### 저장 및 불러오기

kubeflow를 실행하면 발열, 빠른 배터리 소모, 높은 메모리 사용량을 경험하게 됩니다. 맥북의 건강(?)을 위해서 kubeflow를 사용하지 않는 경우 가급적 종료시켜두는 것이 좋습니다.

kubeflow 설치 과정이 다소 번거롭기 때문에 minikube 실행과 동시에 바로 사용할 수 있도록 `minikube stop` 명령어를 이용해 종료하는 것을 권장합니다. colima 또한 'colima stop' 명령어를 통해 종료합니다.

### 파이프라인 구동하기

kubeflow가 정상작동 하는지 확인하기 위해 예제를 활용해 파이프라인을 구동하겠습니다.

먼저 experiment에 들어가 새로운 `create experiment`를 제작합니다.

run 페이지로 이동한 뒤 `creat run`을 클릭합니다.

테스트에 활용할 파이프라인은 ~~~ 입니다.

정상작동했다면 kubeflow 설치가 완료되었습니다.🥳🥳

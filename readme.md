# yaorozu3
# note
# 2024-08-23

### Concept
マルチプロセッシングを取り入れたAlifeシミュレーターのプロトタイプ
マルチプロセシングを利用するためにクラスベースの設計からプロセス関数を直接定義する方式を採用
各プロセス関数（tf_loop、box2d_loop、render_loop）を独立した関数として定義し必要な引数を明示的に渡すようにしています。
Timer関数で、各プロセス関数の周期の差を調整する機構を取り入れています。
共有メモリとプロセス間通信に使用するオブジェクト（shared_positions、shared_forces、rendering_queue、running）をメイン関数内で作成し、各プロセスに引数として渡すようにしています。
初期化処理をシンプルにし、プロセス間で共有できない複雑なオブジェクトの使用を避けました。
KeyboardInterruptを適切に処理し、プロセスを安全に終了できるようにしてあります。

### Trial
高速化のために、tnsorflowをfloat16にするのは失敗。
tensorflowのバッチ化もあまり効果なし。
tensorflowとbox2dの周期を合わせると処理速度が上がった。

**キャッシュの効率的利用:** 同期により、CPUのキャッシュがより効率的に利用されるようになった可能性があります。
**リソースの競合減少:** プロセス間でのCPUやメモリリソースの競合が減少し、各プロセスがより効率的に動作できるようになった可能性があります。
**メモリアクセスの最適化:** プロセス間で交互にメモリにアクセスすることで、メモリバスの利用効率が向上した可能性があります。
**コンテキストスイッチの最適化:** プロセス間のコンテキストスイッチがより規則的かつ効率的になった可能性があります。
**タイミングの最適化:** 各プロセスが最適なタイミングでデータを処理できるようになった可能性があります。
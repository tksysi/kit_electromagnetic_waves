import os
import cmath
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import animatplot as amp

if __name__ == '__main__':
    # 必要に応じて変更するパラメータ
    # --- ここから ---
    
    # 入射角（単位は度, 0 < theta_i < 90）
    theta_i_deg = 60

    # 偏波：'TE' = TE波, 'TM' = TM波
    polarization = 'TE'

    # 媒質1の屈折率
    n1 = 1.41

    # 媒質2の屈折率
    n2 = 1

    # --- ここまで ---

    
    # 定数と関数
    # 複素数に対応するためにcmath内の関数を使用している
    # (「2種媒質の平面境界における反射と屈折」で使用し
    # プログラムを流用したためcmathを使用している）
    PI = cmath.pi
    EXP = cmath.exp
    COS = cmath.cos
    SIN = cmath.sin
    ACOS = cmath.acos
    ASIN = cmath.asin
    SQRT = cmath.sqrt

    
    # 入射角をラジアンに変換
    theta_i = theta_i_deg * PI / 180

    # 反射角
    theta_r = theta_i

    # 反射係数
    if polarization == 'TE':
        R = -1
    else:
        R = 1


    # 正弦波振動1周期に対する分割数
    step_per_period = 20


    # 計算領域の設定
    xx = np.arange(0, 2, 0.01)
    zz = np.arange(-1, 1, 0.01)
    Z, X = np.meshgrid(zz, xx)

    # 総合電界／磁界，入射界，反射界を記録する配列の確保
    F = np.zeros(np.shape(X))
    Fi = np.zeros(np.shape(X))
    Fr = np.zeros(np.shape(X))

    
    fig, ax = plt.subplots(2, 2, figsize=(3,3))

    # subplot間の間隔を設定する
    plt.subplots_adjust(wspace = 0, hspace = 0)

    # 左上のsubplotの軸を非表示にする
    ax[(0,0)].axis('off')


    field_label = {'TE':'$E_y$', 'TM':'$H_y$'}
    
    # 電界／磁界の分布を更新する関数    
    def update(n):
        # 真空中の波の速度
        c = 1

        # 真空中の波長
        wavelength = 1

        # 角周波数
        w = 2 * PI * c / wavelength

        # 周期
        period = 2 * PI / w

        # 描画するための時間の刻み幅
        dt = period / step_per_period

        # 時刻
        t = n * dt

        # 入射波に対する波数ベクトル
        ki = 2 * np.pi / (wavelength / n1)
        kiz = ki * SIN(theta_i)
        kix = -ki * COS(theta_i)

        # 反射波に対する波数ベクトル
        kr = ki
        krz = kr * SIN(theta_r)
        krx = kr * COS(theta_r)


        # 電界／磁界分布の計算
        M, N = np.shape(X)
        F_in_x = np.zeros(M)
        F_in_z = np.zeros(N)
        i0 = int(N/2)
        for i in range(0, M):
            for j in range(0, N):
                z = Z[i][j]
                x = X[i][j]

                # 式(3.1) for TE, (3.23) for TM
                Fi[i][j] = EXP(1j * (w * t - (kiz*z + kix*x))).real

                # 式(3.18) fro TE, (3.24) for TM
                Fr[i][j] = (R * EXP(1j * (w * t - (krz*z + krx*x)))).real

                F_in_z[j] = Fi[i0][j] + Fr[i0][j]

            F_in_x[i] = Fi[i][0] + Fr[i][0]
            
        F = Fi + Fr


        k = (0, 1)
        # scale_factor はグラフの表示を調整するために導入したパラメータ
        # 界分布の振幅を調整してプロットすることでグラフの大きさを
        # 調整しているだけなので，本質的ではない
        scale_factor = 4

        f = F_in_z / scale_factor
        # 入射界の振幅が1のとき総合界Fの振幅は2となる
        # fの振幅は2/scale_factorとなるので表示範囲をそれに合わせている
        flim = (-2/scale_factor, 2/scale_factor)
        
        ax[k].cla()
        ax[k].plot(zz, F_in_z/scale_factor)
        ax[k].set_xlim((-1,1))
        ax[k].set_ylim(flim)
        ax[k].set_xlabel('z')
        ax[k].set_xticks([])
        ax[k].set_ylabel(field_label[polarization])
        ax[k].set_yticks([])
        ax[k].set_aspect(1)
        
        k = (1, 0)
        scale_factor = 4
        f = F_in_x / scale_factor
        flim = (-2/scale_factor, 2/scale_factor)
        ax[k].cla()
        ax[k].plot(f, xx)
        ax[k].set_xlim(flim)
        ax[k].set_ylim((0, 2))
        ax[k].set_xlabel(field_label[polarization])
        ax[k].set_xticks([])
        ax[k].set_ylabel('x')
        ax[k].set_yticks([])
        ax[k].set_aspect(1)

        k = (1, 1)
        ax[k].imshow(F, vmin=-2, vmax=2, cmap='jet')
        ax[k].invert_yaxis()
        ax[k].set_xlabel('z')
        ax[k].set_xticks([])
        ax[k].set_ylabel('x')
        ax[k].set_yticks([])


    # アニメーション表示
    timeline = amp.Timeline(range(0,step_per_period))
    block = amp.blocks.Nuke(update, length=len(timeline))
    anim = amp.Animation([block], timeline)
##    anim.save_gif(os.path.basename(__file__).split('.')[0])
    plt.show()

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
    theta_i_deg = 35.34

    # 偏波：'TE' = TE波, 'TM' = TM波
    polarization = 'TE'

    # 媒質1の屈折率
    n1 = 1.41

    # 媒質2の屈折率
    n2 = 1

    # --- ここまで ---

    
    # 定数と関数
    # 複素数に対応するためにcmath内の関数を使用している
    PI = cmath.pi
    EXP = cmath.exp
    COS = cmath.cos
    SIN = cmath.sin
    ACOS = cmath.acos
    ASIN = cmath.asin
    ATAN = cmath.atan
    SQRT = cmath.sqrt

    
    # 臨界角
    theta_c = ASIN(n2 / n1)

    # ブルースター角
    theta_b = ATAN(n2/n1)
    
    # 入射角をラジアンに変換
    theta_i = theta_i_deg * PI / 180

    # 反射角
    theta_r = theta_i

    # 透過角
    # 全反射する場合は値が複素数になる
    theta_t = ACOS(SQRT(1-(n1*SIN(theta_i)/n2)**2))

    # 反射係数と透過係数
    if polarization == 'TE':
        # 式(3.42)と(3.43)
        R = (1/(n2*COS(theta_t)) - 1/(n1*COS(theta_i))) \
            / (1/(n2*COS(theta_t)) + 1/(n1*COS(theta_i)))
        T = 2 / (n2*COS(theta_t)) \
            / (1/(n2*COS(theta_t)) + 1/(n1*COS(theta_i)))
    else:
        # 式(3.44)と(3.45)
        R = - (COS(theta_t)/n2 - COS(theta_i)/n1) \
            / (COS(theta_t)/n2 + COS(theta_i)/n1)
        T = 2 * COS(theta_i) / n1 \
            / (COS(theta_t)/n2 + COS(theta_i)/n1)


    # 正弦波振動1周期に対する分割数
    step_per_period = 20

    # 臨海角の表示（単位は度）
    print('theta_c = ', theta_c.real * 180 / PI)
    print('theta_b = ', theta_b * 180 / PI)
    

    # 計算領域の設定
    zz = xx = np.arange(-1, 1, 0.01)
    Z, X = np.meshgrid(zz, xx)

    # 総合電界／磁界，入射界，反射界，透過界を記録する配列の確保
    F = np.zeros(np.shape(X))
    Fi = np.zeros(np.shape(X))
    Fr = np.zeros(np.shape(X))
    Ft = np.zeros(np.shape(X))


    fig, ax = plt.subplots(1, 3, figsize=(6,2.5))


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

        # 透過波に対する波数ベクトル
        kt = 2 * PI / (wavelength / n2)
        ktz = kt * SIN(theta_t)
        ktx = -kt * COS(theta_t)
        if ktx.imag < 0:
            # 全反射する場合
            # x < 0の向きに減衰する波数とする
            ktx = ktx.conjugate()

        # 電界／磁界分布の計算
        M, N = np.shape(X)
        for i in range(0, M):
            for j in range(0, N):
                z = Z[i][j]
                x = X[i][j]
                if x >= 0:
                    # 式(3.33)
                    Fi[i][j] = EXP(1j * (w * t - (kiz*z + kix*x))).real

                    # 式(3.35)
                    Fr[i][j] = (R * EXP(1j * (w * t - (krz*z + krx*x)))).real
                if x < 0:
                    # 式(3.37)
                    Ft[i][j] = (T * EXP(1j * (w * t - (ktz*z + ktx*x)))).real
                    
        F = Fi + Fr + Ft

        images = [Fi, F, Fr+Ft]
        titles = ['incident field', 'total field', 
                  'reflected and \ntransmitted fields']
        for i in range(0, len(images)):
            ax[i].imshow(images[i], vmin=-2, vmax=2, cmap='jet')
            ax[i].invert_yaxis()
            ax[i].set_title(titles[i])
            ax[i].set_xlabel('z')
            ax[i].set_xticks([])
            ax[i].set_ylabel('x')
            ax[i].set_yticks([])


    # アニメーション表示
    timeline = amp.Timeline(range(0,step_per_period))
    block = amp.blocks.Nuke(update, length=len(timeline))
    anim = amp.Animation([block], timeline)
    anim.save_gif(os.path.basename(__file__).split('.')[0])
    plt.show()

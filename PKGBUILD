# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# Maintainer: Alone2 <admin@bundr.net>
pkgname=studyFlash
pkgver=0.1
pkgrel=1
pkgdesc="Flashcard in your terminal"
arch=("x86_64")
url="https://github.com/Alone2/studyFlash"
license=('GPL3')
depends=('python' 'python3')
source=("https://github.com/Alone2/studyFlash/archive/v$pkgver.tar.gz")
md5sums=("SKIP")

package() {
	cd "${srcdir}/${pkgname}-${pkgver}"
	install -Dm755 study.py ${pkgdir}/usr/bin/studyFlash
	install -Dm755 getFromQuizlet.py ${pkgdir}/usr/bin/studyFlash-quizlet
}


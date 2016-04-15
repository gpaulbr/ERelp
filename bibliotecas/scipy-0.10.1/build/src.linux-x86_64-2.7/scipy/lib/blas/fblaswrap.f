c     <p2=c,z,c,z> <s2=u,u,c,c> <ftype2=complex,double complex,\0,\1>
      subroutine wcdotu (r, n, x, incx, y, incy)
      external cdotu
      complex cdotu, r
      integer n
      complex x (*)
      integer incx
      complex y (*)
      integer incy
      r = cdotu (n, x, incx, y, incy)
      end


      subroutine wzdotu (r, n, x, incx, y, incy)
      external zdotu
      double complex zdotu, r
      integer n
      double complex x (*)
      integer incx
      double complex y (*)
      integer incy
      r = zdotu (n, x, incx, y, incy)
      end


      subroutine wcdotc (r, n, x, incx, y, incy)
      external cdotc
      complex cdotc, r
      integer n
      complex x (*)
      integer incx
      complex y (*)
      integer incy
      r = cdotc (n, x, incx, y, incy)
      end


      subroutine wzdotc (r, n, x, incx, y, incy)
      external zdotc
      double complex zdotc, r
      integer n
      double complex x (*)
      integer incx
      double complex y (*)
      integer incy
      r = zdotc (n, x, incx, y, incy)
      end



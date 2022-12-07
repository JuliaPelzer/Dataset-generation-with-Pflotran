#ifndef LAPACK_H
#define LAPACK_H

/*
*  Turn on HAVE_LAPACK_CONFIG_H to redefine C-LAPACK datatypes
*/
#ifdef HAVE_LAPACK_CONFIG_H
#include "lapacke_config.h"
#endif

#include "lapacke_mangling.h"

#include <stdlib.h>
#include <stdarg.h>

/* It seems all current Fortran compilers put strlen at end.
*  Some historical compilers put strlen after the str argument
*  or make the str argument into a struct. */
#define LAPACK_FORTRAN_STRLEN_END

/* Complex types are structures equivalent to the
* Fortran complex types COMPLEX(4) and COMPLEX(8).
*
* One can also redefine the types with his own types
* for example by including in the code definitions like
*
* #define lapack_complex_float std::complex<float>
* #define lapack_complex_double std::complex<double>
*
* or define these types in the command line:
*
* -Dlapack_complex_float="std::complex<float>"
* -Dlapack_complex_double="std::complex<double>"
*/

#ifndef LAPACK_COMPLEX_CUSTOM

/* Complex type (single precision) */
#ifndef lapack_complex_float
#ifndef __cplusplus
#include <complex.h>
#else
#include <complex>
#endif
#define lapack_complex_float    float _Complex
#endif

#ifndef lapack_complex_float_real
#define lapack_complex_float_real(z)       (creal(z))
#endif

#ifndef lapack_complex_float_imag
#define lapack_complex_float_imag(z)       (cimag(z))
#endif

/* Complex type (double precision) */
#ifndef lapack_complex_double
#ifndef __cplusplus
#include <complex.h>
#else
#include <complex>
#endif
#define lapack_complex_double   double _Complex
#endif

#ifndef lapack_complex_double_real
#define lapack_complex_double_real(z)      (creal(z))
#endif

#ifndef lapack_complex_double_imag
#define lapack_complex_double_imag(z)       (cimag(z))
#endif

#endif /* LAPACK_COMPLEX_CUSTOM */


#ifdef __cplusplus
extern "C" {
#endif

/*----------------------------------------------------------------------------*/
#ifndef lapack_int
#define lapack_int     int
#endif

#ifndef lapack_logical
#define lapack_logical lapack_int
#endif

/* f2c, hence clapack and MacOS Accelerate, returns double instead of float
 * for sdot, slange, clange, etc. */
#if defined(LAPACK_F2C)
    typedef double lapack_float_return;
#else
    typedef float lapack_float_return;
#endif


/* Callback logical functions of one, two, or three arguments are used
*  to select eigenvalues to sort to the top left of the Schur form.
*  The value is selected if function returns TRUE (non-zero). */

typedef lapack_logical (*LAPACK_S_SELECT2) ( const float*, const float* );
typedef lapack_logical (*LAPACK_S_SELECT3)
    ( const float*, const float*, const float* );
typedef lapack_logical (*LAPACK_D_SELECT2) ( const double*, const double* );
typedef lapack_logical (*LAPACK_D_SELECT3)
    ( const double*, const double*, const double* );

typedef lapack_logical (*LAPACK_C_SELECT1) ( const lapack_complex_float* );
typedef lapack_logical (*LAPACK_C_SELECT2)
    ( const lapack_complex_float*, const lapack_complex_float* );
typedef lapack_logical (*LAPACK_Z_SELECT1) ( const lapack_complex_double* );
typedef lapack_logical (*LAPACK_Z_SELECT2)
    ( const lapack_complex_double*, const lapack_complex_double* );

#define LAPACK_lsame_base LAPACK_GLOBAL(lsame,LSAME)
lapack_logical LAPACK_lsame_base( char* ca,  char* cb,
                              lapack_int lca, lapack_int lcb
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_lsame(...) LAPACK_lsame_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_lsame(...) LAPACK_lsame_base(__VA_ARGS__)
#endif


/*----------------------------------------------------------------------------*/
/* This is in alphabetical order (ignoring leading precision). */

#define LAPACK_cbbcsd_base LAPACK_GLOBAL(cbbcsd,CBBCSD)
void LAPACK_cbbcsd_base(
    char const* jobu1, char const* jobu2, char const* jobv1t, char const* jobv2t, char const* trans,
    lapack_int const* m, lapack_int const* p, lapack_int const* q,
    float* theta,
    float* phi,
    lapack_complex_float* U1, lapack_int const* ldu1,
    lapack_complex_float* U2, lapack_int const* ldu2,
    lapack_complex_float* V1T, lapack_int const* ldv1t,
    lapack_complex_float* V2T, lapack_int const* ldv2t,
    float* B11D,
    float* B11E,
    float* B12D,
    float* B12E,
    float* B21D,
    float* B21E,
    float* B22D,
    float* B22E,
    float* rwork, lapack_int const* lrwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cbbcsd(...) LAPACK_cbbcsd_base(__VA_ARGS__, 1, 1, 1, 1, 1)
#else
    #define LAPACK_cbbcsd(...) LAPACK_cbbcsd_base(__VA_ARGS__)
#endif

#define LAPACK_dbbcsd_base LAPACK_GLOBAL(dbbcsd,DBBCSD)
void LAPACK_dbbcsd_base(
    char const* jobu1, char const* jobu2, char const* jobv1t, char const* jobv2t, char const* trans,
    lapack_int const* m, lapack_int const* p, lapack_int const* q,
    double* theta,
    double* phi,
    double* U1, lapack_int const* ldu1,
    double* U2, lapack_int const* ldu2,
    double* V1T, lapack_int const* ldv1t,
    double* V2T, lapack_int const* ldv2t,
    double* B11D,
    double* B11E,
    double* B12D,
    double* B12E,
    double* b21d,
    double* b21e,
    double* b22d,
    double* b22e,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dbbcsd(...) LAPACK_dbbcsd_base(__VA_ARGS__, 1, 1, 1, 1, 1)
#else
    #define LAPACK_dbbcsd(...) LAPACK_dbbcsd_base(__VA_ARGS__)
#endif

#define LAPACK_sbbcsd_base LAPACK_GLOBAL(sbbcsd,SBBCSD)
void LAPACK_sbbcsd_base(
    char const* jobu1, char const* jobu2, char const* jobv1t, char const* jobv2t, char const* trans,
    lapack_int const* m, lapack_int const* p, lapack_int const* q,
    float* theta,
    float* phi,
    float* U1, lapack_int const* ldu1,
    float* U2, lapack_int const* ldu2,
    float* V1T, lapack_int const* ldv1t,
    float* V2T, lapack_int const* ldv2t,
    float* B11D,
    float* B11E,
    float* B12D,
    float* B12E,
    float* B21D,
    float* B21E,
    float* B22D,
    float* B22E,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sbbcsd(...) LAPACK_sbbcsd_base(__VA_ARGS__, 1, 1, 1, 1, 1)
#else
    #define LAPACK_sbbcsd(...) LAPACK_sbbcsd_base(__VA_ARGS__)
#endif

#define LAPACK_zbbcsd_base LAPACK_GLOBAL(zbbcsd,ZBBCSD)
void LAPACK_zbbcsd_base(
    char const* jobu1, char const* jobu2, char const* jobv1t, char const* jobv2t, char const* trans,
    lapack_int const* m, lapack_int const* p, lapack_int const* q,
    double* theta,
    double* phi,
    lapack_complex_double* U1, lapack_int const* ldu1,
    lapack_complex_double* U2, lapack_int const* ldu2,
    lapack_complex_double* V1T, lapack_int const* ldv1t,
    lapack_complex_double* V2T, lapack_int const* ldv2t,
    double* B11D,
    double* B11E,
    double* B12D,
    double* B12E,
    double* B21D,
    double* B21E,
    double* B22D,
    double* B22E,
    double* rwork, lapack_int const* lrwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zbbcsd(...) LAPACK_zbbcsd_base(__VA_ARGS__, 1, 1, 1, 1, 1)
#else
    #define LAPACK_zbbcsd(...) LAPACK_zbbcsd_base(__VA_ARGS__)
#endif

#define LAPACK_dbdsdc_base LAPACK_GLOBAL(dbdsdc,DBDSDC)
void LAPACK_dbdsdc_base(
    char const* uplo, char const* compq,
    lapack_int const* n,
    double* D,
    double* E,
    double* U, lapack_int const* ldu,
    double* VT, lapack_int const* ldvt,
    double* Q, lapack_int* IQ,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dbdsdc(...) LAPACK_dbdsdc_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dbdsdc(...) LAPACK_dbdsdc_base(__VA_ARGS__)
#endif

#define LAPACK_sbdsdc_base LAPACK_GLOBAL(sbdsdc,SBDSDC)
void LAPACK_sbdsdc_base(
    char const* uplo, char const* compq,
    lapack_int const* n,
    float* D,
    float* E,
    float* U, lapack_int const* ldu,
    float* VT, lapack_int const* ldvt,
    float* Q, lapack_int* IQ,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sbdsdc(...) LAPACK_sbdsdc_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sbdsdc(...) LAPACK_sbdsdc_base(__VA_ARGS__)
#endif

#define LAPACK_cbdsqr_base LAPACK_GLOBAL(cbdsqr,CBDSQR)
void LAPACK_cbdsqr_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* ncvt, lapack_int const* nru, lapack_int const* ncc,
    float* D,
    float* E,
    lapack_complex_float* VT, lapack_int const* ldvt,
    lapack_complex_float* U, lapack_int const* ldu,
    lapack_complex_float* C, lapack_int const* ldc,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cbdsqr(...) LAPACK_cbdsqr_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cbdsqr(...) LAPACK_cbdsqr_base(__VA_ARGS__)
#endif

#define LAPACK_dbdsqr_base LAPACK_GLOBAL(dbdsqr,DBDSQR)
void LAPACK_dbdsqr_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* ncvt, lapack_int const* nru, lapack_int const* ncc,
    double* D,
    double* E,
    double* VT, lapack_int const* ldvt,
    double* U, lapack_int const* ldu,
    double* C, lapack_int const* ldc,
    double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dbdsqr(...) LAPACK_dbdsqr_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dbdsqr(...) LAPACK_dbdsqr_base(__VA_ARGS__)
#endif

#define LAPACK_sbdsqr_base LAPACK_GLOBAL(sbdsqr,SBDSQR)
void LAPACK_sbdsqr_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* ncvt, lapack_int const* nru, lapack_int const* ncc,
    float* D,
    float* E,
    float* VT, lapack_int const* ldvt,
    float* U, lapack_int const* ldu,
    float* C, lapack_int const* ldc,
    float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sbdsqr(...) LAPACK_sbdsqr_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sbdsqr(...) LAPACK_sbdsqr_base(__VA_ARGS__)
#endif

#define LAPACK_zbdsqr_base LAPACK_GLOBAL(zbdsqr,ZBDSQR)
void LAPACK_zbdsqr_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* ncvt, lapack_int const* nru, lapack_int const* ncc,
    double* D,
    double* E,
    lapack_complex_double* VT, lapack_int const* ldvt,
    lapack_complex_double* U, lapack_int const* ldu,
    lapack_complex_double* C, lapack_int const* ldc,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zbdsqr(...) LAPACK_zbdsqr_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zbdsqr(...) LAPACK_zbdsqr_base(__VA_ARGS__)
#endif

#define LAPACK_dbdsvdx_base LAPACK_GLOBAL(dbdsvdx,DBDSVDX)
void LAPACK_dbdsvdx_base(
    char const* uplo, char const* jobz, char const* range,
    lapack_int const* n,
    double const* D,
    double const* E,
    double const* vl,
    double const* vu, lapack_int const* il, lapack_int const* iu, lapack_int* ns,
    double* S,
    double* Z, lapack_int const* ldz,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dbdsvdx(...) LAPACK_dbdsvdx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dbdsvdx(...) LAPACK_dbdsvdx_base(__VA_ARGS__)
#endif

#define LAPACK_sbdsvdx_base LAPACK_GLOBAL(sbdsvdx,SBDSVDX)
void LAPACK_sbdsvdx_base(
    char const* uplo, char const* jobz, char const* range,
    lapack_int const* n,
    float const* D,
    float const* E,
    float const* vl,
    float const* vu, lapack_int const* il, lapack_int const* iu, lapack_int* ns,
    float* S,
    float* Z, lapack_int const* ldz,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sbdsvdx(...) LAPACK_sbdsvdx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sbdsvdx(...) LAPACK_sbdsvdx_base(__VA_ARGS__)
#endif

#define LAPACK_ddisna_base LAPACK_GLOBAL(ddisna,DDISNA)
void LAPACK_ddisna_base(
    char const* job,
    lapack_int const* m, lapack_int const* n,
    double const* D,
    double* SEP,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_ddisna(...) LAPACK_ddisna_base(__VA_ARGS__, 1)
#else
    #define LAPACK_ddisna(...) LAPACK_ddisna_base(__VA_ARGS__)
#endif

#define LAPACK_sdisna_base LAPACK_GLOBAL(sdisna,SDISNA)
void LAPACK_sdisna_base(
    char const* job,
    lapack_int const* m, lapack_int const* n,
    float const* D,
    float* SEP,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sdisna(...) LAPACK_sdisna_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sdisna(...) LAPACK_sdisna_base(__VA_ARGS__)
#endif

#define LAPACK_cgbbrd_base LAPACK_GLOBAL(cgbbrd,CGBBRD)
void LAPACK_cgbbrd_base(
    char const* vect,
    lapack_int const* m, lapack_int const* n, lapack_int const* ncc, lapack_int const* kl, lapack_int const* ku,
    lapack_complex_float* AB, lapack_int const* ldab,
    float* D,
    float* E,
    lapack_complex_float* Q, lapack_int const* ldq,
    lapack_complex_float* PT, lapack_int const* ldpt,
    lapack_complex_float* C, lapack_int const* ldc,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgbbrd(...) LAPACK_cgbbrd_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgbbrd(...) LAPACK_cgbbrd_base(__VA_ARGS__)
#endif

#define LAPACK_dgbbrd_base LAPACK_GLOBAL(dgbbrd,DGBBRD)
void LAPACK_dgbbrd_base(
    char const* vect,
    lapack_int const* m, lapack_int const* n, lapack_int const* ncc, lapack_int const* kl, lapack_int const* ku,
    double* AB, lapack_int const* ldab,
    double* D,
    double* E,
    double* Q, lapack_int const* ldq,
    double* PT, lapack_int const* ldpt,
    double* C, lapack_int const* ldc,
    double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgbbrd(...) LAPACK_dgbbrd_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgbbrd(...) LAPACK_dgbbrd_base(__VA_ARGS__)
#endif

#define LAPACK_sgbbrd_base LAPACK_GLOBAL(sgbbrd,SGBBRD)
void LAPACK_sgbbrd_base(
    char const* vect,
    lapack_int const* m, lapack_int const* n, lapack_int const* ncc, lapack_int const* kl, lapack_int const* ku,
    float* AB, lapack_int const* ldab,
    float* D,
    float* E,
    float* Q, lapack_int const* ldq,
    float* PT, lapack_int const* ldpt,
    float* C, lapack_int const* ldc,
    float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgbbrd(...) LAPACK_sgbbrd_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgbbrd(...) LAPACK_sgbbrd_base(__VA_ARGS__)
#endif

#define LAPACK_zgbbrd_base LAPACK_GLOBAL(zgbbrd,ZGBBRD)
void LAPACK_zgbbrd_base(
    char const* vect,
    lapack_int const* m, lapack_int const* n, lapack_int const* ncc, lapack_int const* kl, lapack_int const* ku,
    lapack_complex_double* AB, lapack_int const* ldab,
    double* D,
    double* E,
    lapack_complex_double* Q, lapack_int const* ldq,
    lapack_complex_double* PT, lapack_int const* ldpt,
    lapack_complex_double* C, lapack_int const* ldc,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgbbrd(...) LAPACK_zgbbrd_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgbbrd(...) LAPACK_zgbbrd_base(__VA_ARGS__)
#endif

#define LAPACK_cgbcon_base LAPACK_GLOBAL(cgbcon,CGBCON)
void LAPACK_cgbcon_base(
    char const* norm,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    lapack_complex_float const* AB, lapack_int const* ldab, lapack_int const* ipiv,
    float const* anorm,
    float* rcond,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgbcon(...) LAPACK_cgbcon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgbcon(...) LAPACK_cgbcon_base(__VA_ARGS__)
#endif

#define LAPACK_dgbcon_base LAPACK_GLOBAL(dgbcon,DGBCON)
void LAPACK_dgbcon_base(
    char const* norm,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    double const* AB, lapack_int const* ldab, lapack_int const* ipiv,
    double const* anorm,
    double* rcond,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgbcon(...) LAPACK_dgbcon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgbcon(...) LAPACK_dgbcon_base(__VA_ARGS__)
#endif

#define LAPACK_sgbcon_base LAPACK_GLOBAL(sgbcon,SGBCON)
void LAPACK_sgbcon_base(
    char const* norm,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    float const* AB, lapack_int const* ldab, lapack_int const* ipiv,
    float const* anorm,
    float* rcond,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgbcon(...) LAPACK_sgbcon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgbcon(...) LAPACK_sgbcon_base(__VA_ARGS__)
#endif

#define LAPACK_zgbcon_base LAPACK_GLOBAL(zgbcon,ZGBCON)
void LAPACK_zgbcon_base(
    char const* norm,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    lapack_complex_double const* AB, lapack_int const* ldab, lapack_int const* ipiv,
    double const* anorm,
    double* rcond,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgbcon(...) LAPACK_zgbcon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgbcon(...) LAPACK_zgbcon_base(__VA_ARGS__)
#endif

#define LAPACK_cgbequ LAPACK_GLOBAL(cgbequ,CGBEQU)
void LAPACK_cgbequ(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    lapack_complex_float const* AB, lapack_int const* ldab,
    float* R,
    float* C,
    float* rowcnd,
    float* colcnd,
    float* amax,
    lapack_int* info );

#define LAPACK_dgbequ LAPACK_GLOBAL(dgbequ,DGBEQU)
void LAPACK_dgbequ(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    double const* AB, lapack_int const* ldab,
    double* R,
    double* C,
    double* rowcnd,
    double* colcnd,
    double* amax,
    lapack_int* info );

#define LAPACK_sgbequ LAPACK_GLOBAL(sgbequ,SGBEQU)
void LAPACK_sgbequ(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    float const* AB, lapack_int const* ldab,
    float* R,
    float* C,
    float* rowcnd,
    float* colcnd,
    float* amax,
    lapack_int* info );

#define LAPACK_zgbequ LAPACK_GLOBAL(zgbequ,ZGBEQU)
void LAPACK_zgbequ(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    lapack_complex_double const* AB, lapack_int const* ldab,
    double* R,
    double* C,
    double* rowcnd,
    double* colcnd,
    double* amax,
    lapack_int* info );

#define LAPACK_cgbequb LAPACK_GLOBAL(cgbequb,CGBEQUB)
void LAPACK_cgbequb(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    lapack_complex_float const* AB, lapack_int const* ldab,
    float* R,
    float* C,
    float* rowcnd,
    float* colcnd,
    float* amax,
    lapack_int* info );

#define LAPACK_dgbequb LAPACK_GLOBAL(dgbequb,DGBEQUB)
void LAPACK_dgbequb(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    double const* AB, lapack_int const* ldab,
    double* R,
    double* C,
    double* rowcnd,
    double* colcnd,
    double* amax,
    lapack_int* info );

#define LAPACK_sgbequb LAPACK_GLOBAL(sgbequb,SGBEQUB)
void LAPACK_sgbequb(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    float const* AB, lapack_int const* ldab,
    float* R,
    float* C,
    float* rowcnd,
    float* colcnd,
    float* amax,
    lapack_int* info );

#define LAPACK_zgbequb LAPACK_GLOBAL(zgbequb,ZGBEQUB)
void LAPACK_zgbequb(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    lapack_complex_double const* AB, lapack_int const* ldab,
    double* R,
    double* C,
    double* rowcnd,
    double* colcnd,
    double* amax,
    lapack_int* info );

#define LAPACK_cgbrfs_base LAPACK_GLOBAL(cgbrfs,CGBRFS)
void LAPACK_cgbrfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_float const* AB, lapack_int const* ldab,
    lapack_complex_float const* AFB, lapack_int const* ldafb, lapack_int const* ipiv,
    lapack_complex_float const* B, lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* ferr,
    float* berr,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgbrfs(...) LAPACK_cgbrfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgbrfs(...) LAPACK_cgbrfs_base(__VA_ARGS__)
#endif

#define LAPACK_dgbrfs_base LAPACK_GLOBAL(dgbrfs,DGBRFS)
void LAPACK_dgbrfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    double const* AB, lapack_int const* ldab,
    double const* AFB, lapack_int const* ldafb, lapack_int const* ipiv,
    double const* B, lapack_int const* ldb,
    double* X, lapack_int const* ldx,
    double* ferr,
    double* berr,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgbrfs(...) LAPACK_dgbrfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgbrfs(...) LAPACK_dgbrfs_base(__VA_ARGS__)
#endif

#define LAPACK_sgbrfs_base LAPACK_GLOBAL(sgbrfs,SGBRFS)
void LAPACK_sgbrfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    float const* AB, lapack_int const* ldab,
    float const* AFB, lapack_int const* ldafb, lapack_int const* ipiv,
    float const* B, lapack_int const* ldb,
    float* X, lapack_int const* ldx,
    float* ferr,
    float* berr,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgbrfs(...) LAPACK_sgbrfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgbrfs(...) LAPACK_sgbrfs_base(__VA_ARGS__)
#endif

#define LAPACK_zgbrfs_base LAPACK_GLOBAL(zgbrfs,ZGBRFS)
void LAPACK_zgbrfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_double const* AB, lapack_int const* ldab,
    lapack_complex_double const* AFB, lapack_int const* ldafb, lapack_int const* ipiv,
    lapack_complex_double const* B, lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* ferr,
    double* berr,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgbrfs(...) LAPACK_zgbrfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgbrfs(...) LAPACK_zgbrfs_base(__VA_ARGS__)
#endif

#define LAPACK_cgbrfsx_base LAPACK_GLOBAL(cgbrfsx,CGBRFSX)
void LAPACK_cgbrfsx_base(
    char const* trans, char const* equed,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_float const* AB, lapack_int const* ldab,
    lapack_complex_float const* AFB, lapack_int const* ldafb, lapack_int const* ipiv,
    const float* R,
    const float* C,
    lapack_complex_float const* B, lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* rcond,
    float* berr, lapack_int const* n_err_bnds,
    float* err_bnds_norm,
    float* err_bnds_comp, lapack_int const* nparams,
    float* params,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgbrfsx(...) LAPACK_cgbrfsx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgbrfsx(...) LAPACK_cgbrfsx_base(__VA_ARGS__)
#endif

#define LAPACK_dgbrfsx_base LAPACK_GLOBAL(dgbrfsx,DGBRFSX)
void LAPACK_dgbrfsx_base(
    char const* trans, char const* equed,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    double const* AB, lapack_int const* ldab,
    double const* AFB, lapack_int const* ldafb, lapack_int const* ipiv,
    const double* R,
    const double* C,
    double const* B, lapack_int const* ldb,
    double* X, lapack_int const* ldx,
    double* rcond,
    double* berr, lapack_int const* n_err_bnds,
    double* err_bnds_norm,
    double* err_bnds_comp, lapack_int const* nparams,
    double* params,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgbrfsx(...) LAPACK_dgbrfsx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgbrfsx(...) LAPACK_dgbrfsx_base(__VA_ARGS__)
#endif

#define LAPACK_sgbrfsx_base LAPACK_GLOBAL(sgbrfsx,SGBRFSX)
void LAPACK_sgbrfsx_base(
    char const* trans, char const* equed,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    float const* AB, lapack_int const* ldab,
    float const* AFB, lapack_int const* ldafb, lapack_int const* ipiv,
    const float* R,
    const float* C,
    float const* B, lapack_int const* ldb,
    float* X, lapack_int const* ldx,
    float* rcond,
    float* berr, lapack_int const* n_err_bnds,
    float* err_bnds_norm,
    float* err_bnds_comp, lapack_int const* nparams,
    float* params,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgbrfsx(...) LAPACK_sgbrfsx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgbrfsx(...) LAPACK_sgbrfsx_base(__VA_ARGS__)
#endif

#define LAPACK_zgbrfsx_base LAPACK_GLOBAL(zgbrfsx,ZGBRFSX)
void LAPACK_zgbrfsx_base(
    char const* trans, char const* equed,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_double const* AB, lapack_int const* ldab,
    lapack_complex_double const* AFB, lapack_int const* ldafb, lapack_int const* ipiv,
    const double* R,
    const double* C,
    lapack_complex_double const* B, lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* rcond,
    double* berr, lapack_int const* n_err_bnds,
    double* err_bnds_norm,
    double* err_bnds_comp, lapack_int const* nparams,
    double* params,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgbrfsx(...) LAPACK_zgbrfsx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgbrfsx(...) LAPACK_zgbrfsx_base(__VA_ARGS__)
#endif

#define LAPACK_cgbsv LAPACK_GLOBAL(cgbsv,CGBSV)
void LAPACK_cgbsv(
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_float* AB, lapack_int const* ldab, lapack_int* ipiv,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_dgbsv LAPACK_GLOBAL(dgbsv,DGBSV)
void LAPACK_dgbsv(
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    double* AB, lapack_int const* ldab, lapack_int* ipiv,
    double* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_sgbsv LAPACK_GLOBAL(sgbsv,SGBSV)
void LAPACK_sgbsv(
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    float* AB, lapack_int const* ldab, lapack_int* ipiv,
    float* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_zgbsv LAPACK_GLOBAL(zgbsv,ZGBSV)
void LAPACK_zgbsv(
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_double* AB, lapack_int const* ldab, lapack_int* ipiv,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_cgbsvx_base LAPACK_GLOBAL(cgbsvx,CGBSVX)
void LAPACK_cgbsvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_float* AB, lapack_int const* ldab,
    lapack_complex_float* AFB, lapack_int const* ldafb, lapack_int* ipiv, char* equed,
    float* R,
    float* C,
    lapack_complex_float* B,
    lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* rcond,
    float* ferr,
    float* berr,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgbsvx(...) LAPACK_cgbsvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cgbsvx(...) LAPACK_cgbsvx_base(__VA_ARGS__)
#endif

#define LAPACK_dgbsvx_base LAPACK_GLOBAL(dgbsvx,DGBSVX)
void LAPACK_dgbsvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    double* AB, lapack_int const* ldab,
    double* AFB, lapack_int const* ldafb, lapack_int* ipiv, char* equed,
    double* R,
    double* C,
    double* B,
    lapack_int const* ldb,
    double* X, lapack_int const* ldx,
    double* rcond,
    double* ferr,
    double* berr,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgbsvx(...) LAPACK_dgbsvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dgbsvx(...) LAPACK_dgbsvx_base(__VA_ARGS__)
#endif

#define LAPACK_sgbsvx_base LAPACK_GLOBAL(sgbsvx,SGBSVX)
void LAPACK_sgbsvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    float* AB, lapack_int const* ldab,
    float* AFB, lapack_int const* ldafb, lapack_int* ipiv, char* equed,
    float* R,
    float* C,
    float* B,
    lapack_int const* ldb,
    float* X, lapack_int const* ldx,
    float* rcond,
    float* ferr,
    float* berr,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgbsvx(...) LAPACK_sgbsvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sgbsvx(...) LAPACK_sgbsvx_base(__VA_ARGS__)
#endif

#define LAPACK_zgbsvx_base LAPACK_GLOBAL(zgbsvx,ZGBSVX)
void LAPACK_zgbsvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_double* AB, lapack_int const* ldab,
    lapack_complex_double* AFB, lapack_int const* ldafb, lapack_int* ipiv, char* equed,
    double* R,
    double* C,
    lapack_complex_double* B,
    lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* rcond,
    double* ferr,
    double* berr,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgbsvx(...) LAPACK_zgbsvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zgbsvx(...) LAPACK_zgbsvx_base(__VA_ARGS__)
#endif

#define LAPACK_cgbsvxx_base LAPACK_GLOBAL(cgbsvxx,CGBSVXX)
void LAPACK_cgbsvxx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_float* AB, lapack_int const* ldab,
    lapack_complex_float* AFB, lapack_int const* ldafb, lapack_int* ipiv, char* equed,
    float* R,
    float* C,
    lapack_complex_float* B,
    lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* rcond,
    float* rpvgrw,
    float* berr, lapack_int const* n_err_bnds,
    float* err_bnds_norm,
    float* err_bnds_comp, lapack_int const* nparams,
    float* params,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgbsvxx(...) LAPACK_cgbsvxx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cgbsvxx(...) LAPACK_cgbsvxx_base(__VA_ARGS__)
#endif

#define LAPACK_dgbsvxx_base LAPACK_GLOBAL(dgbsvxx,DGBSVXX)
void LAPACK_dgbsvxx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    double* AB, lapack_int const* ldab,
    double* AFB, lapack_int const* ldafb, lapack_int* ipiv, char* equed,
    double* R,
    double* C,
    double* B,
    lapack_int const* ldb,
    double* X, lapack_int const* ldx,
    double* rcond,
    double* rpvgrw,
    double* berr, lapack_int const* n_err_bnds,
    double* err_bnds_norm,
    double* err_bnds_comp, lapack_int const* nparams,
    double* params,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgbsvxx(...) LAPACK_dgbsvxx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dgbsvxx(...) LAPACK_dgbsvxx_base(__VA_ARGS__)
#endif

#define LAPACK_sgbsvxx_base LAPACK_GLOBAL(sgbsvxx,SGBSVXX)
void LAPACK_sgbsvxx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    float* AB, lapack_int const* ldab,
    float* AFB, lapack_int const* ldafb, lapack_int* ipiv, char* equed,
    float* R,
    float* C,
    float* B,
    lapack_int const* ldb,
    float* X, lapack_int const* ldx,
    float* rcond,
    float* rpvgrw,
    float* berr, lapack_int const* n_err_bnds,
    float* err_bnds_norm,
    float* err_bnds_comp, lapack_int const* nparams,
    float* params,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgbsvxx(...) LAPACK_sgbsvxx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sgbsvxx(...) LAPACK_sgbsvxx_base(__VA_ARGS__)
#endif

#define LAPACK_zgbsvxx_base LAPACK_GLOBAL(zgbsvxx,ZGBSVXX)
void LAPACK_zgbsvxx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_double* AB, lapack_int const* ldab,
    lapack_complex_double* AFB, lapack_int const* ldafb, lapack_int* ipiv, char* equed,
    double* R,
    double* C,
    lapack_complex_double* B,
    lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* rcond,
    double* rpvgrw,
    double* berr, lapack_int const* n_err_bnds,
    double* err_bnds_norm,
    double* err_bnds_comp, lapack_int const* nparams,
    double* params,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgbsvxx(...) LAPACK_zgbsvxx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zgbsvxx(...) LAPACK_zgbsvxx_base(__VA_ARGS__)
#endif

#define LAPACK_cgbtrf LAPACK_GLOBAL(cgbtrf,CGBTRF)
void LAPACK_cgbtrf(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    lapack_complex_float* AB, lapack_int const* ldab, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_dgbtrf LAPACK_GLOBAL(dgbtrf,DGBTRF)
void LAPACK_dgbtrf(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    double* AB, lapack_int const* ldab, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_sgbtrf LAPACK_GLOBAL(sgbtrf,SGBTRF)
void LAPACK_sgbtrf(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    float* AB, lapack_int const* ldab, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_zgbtrf LAPACK_GLOBAL(zgbtrf,ZGBTRF)
void LAPACK_zgbtrf(
    lapack_int const* m, lapack_int const* n, lapack_int const* kl, lapack_int const* ku,
    lapack_complex_double* AB, lapack_int const* ldab, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_cgbtrs_base LAPACK_GLOBAL(cgbtrs,CGBTRS)
void LAPACK_cgbtrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_float const* AB, lapack_int const* ldab, lapack_int const* ipiv,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgbtrs(...) LAPACK_cgbtrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgbtrs(...) LAPACK_cgbtrs_base(__VA_ARGS__)
#endif

#define LAPACK_dgbtrs_base LAPACK_GLOBAL(dgbtrs,DGBTRS)
void LAPACK_dgbtrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    double const* AB, lapack_int const* ldab, lapack_int const* ipiv,
    double* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgbtrs(...) LAPACK_dgbtrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgbtrs(...) LAPACK_dgbtrs_base(__VA_ARGS__)
#endif

#define LAPACK_sgbtrs_base LAPACK_GLOBAL(sgbtrs,SGBTRS)
void LAPACK_sgbtrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    float const* AB, lapack_int const* ldab, lapack_int const* ipiv,
    float* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgbtrs(...) LAPACK_sgbtrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgbtrs(...) LAPACK_sgbtrs_base(__VA_ARGS__)
#endif

#define LAPACK_zgbtrs_base LAPACK_GLOBAL(zgbtrs,ZGBTRS)
void LAPACK_zgbtrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* kl, lapack_int const* ku, lapack_int const* nrhs,
    lapack_complex_double const* AB, lapack_int const* ldab, lapack_int const* ipiv,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgbtrs(...) LAPACK_zgbtrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgbtrs(...) LAPACK_zgbtrs_base(__VA_ARGS__)
#endif

#define LAPACK_cgebak_base LAPACK_GLOBAL(cgebak,CGEBAK)
void LAPACK_cgebak_base(
    char const* job, char const* side,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    float const* scale, lapack_int const* m,
    lapack_complex_float* V, lapack_int const* ldv,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgebak(...) LAPACK_cgebak_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgebak(...) LAPACK_cgebak_base(__VA_ARGS__)
#endif

#define LAPACK_dgebak_base LAPACK_GLOBAL(dgebak,DGEBAK)
void LAPACK_dgebak_base(
    char const* job, char const* side,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    double const* scale, lapack_int const* m,
    double* V, lapack_int const* ldv,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgebak(...) LAPACK_dgebak_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgebak(...) LAPACK_dgebak_base(__VA_ARGS__)
#endif

#define LAPACK_sgebak_base LAPACK_GLOBAL(sgebak,SGEBAK)
void LAPACK_sgebak_base(
    char const* job, char const* side,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    float const* scale, lapack_int const* m,
    float* V, lapack_int const* ldv,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgebak(...) LAPACK_sgebak_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgebak(...) LAPACK_sgebak_base(__VA_ARGS__)
#endif

#define LAPACK_zgebak_base LAPACK_GLOBAL(zgebak,ZGEBAK)
void LAPACK_zgebak_base(
    char const* job, char const* side,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    double const* scale, lapack_int const* m,
    lapack_complex_double* V, lapack_int const* ldv,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgebak(...) LAPACK_zgebak_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgebak(...) LAPACK_zgebak_base(__VA_ARGS__)
#endif

#define LAPACK_cgebal_base LAPACK_GLOBAL(cgebal,CGEBAL)
void LAPACK_cgebal_base(
    char const* job,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* ilo, lapack_int* ihi,
    float* scale,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgebal(...) LAPACK_cgebal_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgebal(...) LAPACK_cgebal_base(__VA_ARGS__)
#endif

#define LAPACK_dgebal_base LAPACK_GLOBAL(dgebal,DGEBAL)
void LAPACK_dgebal_base(
    char const* job,
    lapack_int const* n,
    double* A, lapack_int const* lda, lapack_int* ilo, lapack_int* ihi,
    double* scale,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgebal(...) LAPACK_dgebal_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgebal(...) LAPACK_dgebal_base(__VA_ARGS__)
#endif

#define LAPACK_sgebal_base LAPACK_GLOBAL(sgebal,SGEBAL)
void LAPACK_sgebal_base(
    char const* job,
    lapack_int const* n,
    float* A, lapack_int const* lda, lapack_int* ilo, lapack_int* ihi,
    float* scale,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgebal(...) LAPACK_sgebal_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgebal(...) LAPACK_sgebal_base(__VA_ARGS__)
#endif

#define LAPACK_zgebal_base LAPACK_GLOBAL(zgebal,ZGEBAL)
void LAPACK_zgebal_base(
    char const* job,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ilo, lapack_int* ihi,
    double* scale,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgebal(...) LAPACK_zgebal_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgebal(...) LAPACK_zgebal_base(__VA_ARGS__)
#endif

#define LAPACK_cgebrd LAPACK_GLOBAL(cgebrd,CGEBRD)
void LAPACK_cgebrd(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* D,
    float* E,
    lapack_complex_float* tauq,
    lapack_complex_float* taup,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgebrd LAPACK_GLOBAL(dgebrd,DGEBRD)
void LAPACK_dgebrd(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* D,
    double* E,
    double* tauq,
    double* taup,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgebrd LAPACK_GLOBAL(sgebrd,SGEBRD)
void LAPACK_sgebrd(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* D,
    float* E,
    float* tauq,
    float* taup,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgebrd LAPACK_GLOBAL(zgebrd,ZGEBRD)
void LAPACK_zgebrd(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* D,
    double* E,
    lapack_complex_double* tauq,
    lapack_complex_double* taup,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cgecon_base LAPACK_GLOBAL(cgecon,CGECON)
void LAPACK_cgecon_base(
    char const* norm,
    lapack_int const* n,
    lapack_complex_float const* A, lapack_int const* lda,
    float const* anorm,
    float* rcond,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgecon(...) LAPACK_cgecon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgecon(...) LAPACK_cgecon_base(__VA_ARGS__)
#endif

#define LAPACK_dgecon_base LAPACK_GLOBAL(dgecon,DGECON)
void LAPACK_dgecon_base(
    char const* norm,
    lapack_int const* n,
    double const* A, lapack_int const* lda,
    double const* anorm,
    double* rcond,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgecon(...) LAPACK_dgecon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgecon(...) LAPACK_dgecon_base(__VA_ARGS__)
#endif

#define LAPACK_sgecon_base LAPACK_GLOBAL(sgecon,SGECON)
void LAPACK_sgecon_base(
    char const* norm,
    lapack_int const* n,
    float const* A, lapack_int const* lda,
    float const* anorm,
    float* rcond,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgecon(...) LAPACK_sgecon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgecon(...) LAPACK_sgecon_base(__VA_ARGS__)
#endif

#define LAPACK_zgecon_base LAPACK_GLOBAL(zgecon,ZGECON)
void LAPACK_zgecon_base(
    char const* norm,
    lapack_int const* n,
    lapack_complex_double const* A, lapack_int const* lda,
    double const* anorm,
    double* rcond,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgecon(...) LAPACK_zgecon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgecon(...) LAPACK_zgecon_base(__VA_ARGS__)
#endif

#define LAPACK_cgeequ LAPACK_GLOBAL(cgeequ,CGEEQU)
void LAPACK_cgeequ(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float const* A, lapack_int const* lda,
    float* R,
    float* C,
    float* rowcnd,
    float* colcnd,
    float* amax,
    lapack_int* info );

#define LAPACK_dgeequ LAPACK_GLOBAL(dgeequ,DGEEQU)
void LAPACK_dgeequ(
    lapack_int const* m, lapack_int const* n,
    double const* A, lapack_int const* lda,
    double* R,
    double* C,
    double* rowcnd,
    double* colcnd,
    double* amax,
    lapack_int* info );

#define LAPACK_sgeequ LAPACK_GLOBAL(sgeequ,SGEEQU)
void LAPACK_sgeequ(
    lapack_int const* m, lapack_int const* n,
    float const* A, lapack_int const* lda,
    float* R,
    float* C,
    float* rowcnd,
    float* colcnd,
    float* amax,
    lapack_int* info );

#define LAPACK_zgeequ LAPACK_GLOBAL(zgeequ,ZGEEQU)
void LAPACK_zgeequ(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double const* A, lapack_int const* lda,
    double* R,
    double* C,
    double* rowcnd,
    double* colcnd,
    double* amax,
    lapack_int* info );

#define LAPACK_cgeequb LAPACK_GLOBAL(cgeequb,CGEEQUB)
void LAPACK_cgeequb(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float const* A, lapack_int const* lda,
    float* R,
    float* C,
    float* rowcnd,
    float* colcnd,
    float* amax,
    lapack_int* info );

#define LAPACK_dgeequb LAPACK_GLOBAL(dgeequb,DGEEQUB)
void LAPACK_dgeequb(
    lapack_int const* m, lapack_int const* n,
    double const* A, lapack_int const* lda,
    double* R,
    double* C,
    double* rowcnd,
    double* colcnd,
    double* amax,
    lapack_int* info );

#define LAPACK_sgeequb LAPACK_GLOBAL(sgeequb,SGEEQUB)
void LAPACK_sgeequb(
    lapack_int const* m, lapack_int const* n,
    float const* A, lapack_int const* lda,
    float* R,
    float* C,
    float* rowcnd,
    float* colcnd,
    float* amax,
    lapack_int* info );

#define LAPACK_zgeequb LAPACK_GLOBAL(zgeequb,ZGEEQUB)
void LAPACK_zgeequb(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double const* A, lapack_int const* lda,
    double* R,
    double* C,
    double* rowcnd,
    double* colcnd,
    double* amax,
    lapack_int* info );

#define LAPACK_cgees_base LAPACK_GLOBAL(cgees,CGEES)
void LAPACK_cgees_base(
    char const* jobvs, char const* sort, LAPACK_C_SELECT1 select,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* sdim,
    lapack_complex_float* W,
    lapack_complex_float* VS, lapack_int const* ldvs,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgees(...) LAPACK_cgees_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgees(...) LAPACK_cgees_base(__VA_ARGS__)
#endif

#define LAPACK_dgees_base LAPACK_GLOBAL(dgees,DGEES)
void LAPACK_dgees_base(
    char const* jobvs, char const* sort, LAPACK_D_SELECT2 select,
    lapack_int const* n,
    double* A, lapack_int const* lda, lapack_int* sdim,
    double* WR,
    double* WI,
    double* VS, lapack_int const* ldvs,
    double* work, lapack_int const* lwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgees(...) LAPACK_dgees_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgees(...) LAPACK_dgees_base(__VA_ARGS__)
#endif

#define LAPACK_sgees_base LAPACK_GLOBAL(sgees,SGEES)
void LAPACK_sgees_base(
    char const* jobvs, char const* sort, LAPACK_S_SELECT2 select,
    lapack_int const* n,
    float* A, lapack_int const* lda, lapack_int* sdim,
    float* WR,
    float* WI,
    float* VS, lapack_int const* ldvs,
    float* work, lapack_int const* lwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgees(...) LAPACK_sgees_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgees(...) LAPACK_sgees_base(__VA_ARGS__)
#endif

#define LAPACK_zgees_base LAPACK_GLOBAL(zgees,ZGEES)
void LAPACK_zgees_base(
    char const* jobvs, char const* sort, LAPACK_Z_SELECT1 select,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* sdim,
    lapack_complex_double* W,
    lapack_complex_double* VS, lapack_int const* ldvs,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgees(...) LAPACK_zgees_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgees(...) LAPACK_zgees_base(__VA_ARGS__)
#endif

#define LAPACK_cgeesx_base LAPACK_GLOBAL(cgeesx,CGEESX)
void LAPACK_cgeesx_base(
    char const* jobvs, char const* sort, LAPACK_C_SELECT1 select, char const* sense,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* sdim,
    lapack_complex_float* W,
    lapack_complex_float* VS, lapack_int const* ldvs,
    float* rconde,
    float* rcondv,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgeesx(...) LAPACK_cgeesx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cgeesx(...) LAPACK_cgeesx_base(__VA_ARGS__)
#endif

#define LAPACK_dgeesx_base LAPACK_GLOBAL(dgeesx,DGEESX)
void LAPACK_dgeesx_base(
    char const* jobvs, char const* sort, LAPACK_D_SELECT2 select, char const* sense,
    lapack_int const* n,
    double* A, lapack_int const* lda, lapack_int* sdim,
    double* WR,
    double* WI,
    double* VS, lapack_int const* ldvs,
    double* rconde,
    double* rcondv,
    double* work, lapack_int const* lwork,
    lapack_int* iwork, lapack_int const* liwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgeesx(...) LAPACK_dgeesx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dgeesx(...) LAPACK_dgeesx_base(__VA_ARGS__)
#endif

#define LAPACK_sgeesx_base LAPACK_GLOBAL(sgeesx,SGEESX)
void LAPACK_sgeesx_base(
    char const* jobvs, char const* sort, LAPACK_S_SELECT2 select, char const* sense,
    lapack_int const* n,
    float* A, lapack_int const* lda, lapack_int* sdim,
    float* WR,
    float* WI,
    float* VS, lapack_int const* ldvs,
    float* rconde,
    float* rcondv,
    float* work, lapack_int const* lwork,
    lapack_int* iwork, lapack_int const* liwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgeesx(...) LAPACK_sgeesx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sgeesx(...) LAPACK_sgeesx_base(__VA_ARGS__)
#endif

#define LAPACK_zgeesx_base LAPACK_GLOBAL(zgeesx,ZGEESX)
void LAPACK_zgeesx_base(
    char const* jobvs, char const* sort, LAPACK_Z_SELECT1 select, char const* sense,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* sdim,
    lapack_complex_double* W,
    lapack_complex_double* VS, lapack_int const* ldvs,
    double* rconde,
    double* rcondv,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgeesx(...) LAPACK_zgeesx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zgeesx(...) LAPACK_zgeesx_base(__VA_ARGS__)
#endif

#define LAPACK_cgeev_base LAPACK_GLOBAL(cgeev,CGEEV)
void LAPACK_cgeev_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* W,
    lapack_complex_float* VL, lapack_int const* ldvl,
    lapack_complex_float* VR, lapack_int const* ldvr,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgeev(...) LAPACK_cgeev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgeev(...) LAPACK_cgeev_base(__VA_ARGS__)
#endif

#define LAPACK_dgeev_base LAPACK_GLOBAL(dgeev,DGEEV)
void LAPACK_dgeev_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    double* A, lapack_int const* lda,
    double* WR,
    double* WI,
    double* VL, lapack_int const* ldvl,
    double* VR, lapack_int const* ldvr,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgeev(...) LAPACK_dgeev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgeev(...) LAPACK_dgeev_base(__VA_ARGS__)
#endif

#define LAPACK_sgeev_base LAPACK_GLOBAL(sgeev,SGEEV)
void LAPACK_sgeev_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    float* A, lapack_int const* lda,
    float* WR,
    float* WI,
    float* VL, lapack_int const* ldvl,
    float* VR, lapack_int const* ldvr,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgeev(...) LAPACK_sgeev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgeev(...) LAPACK_sgeev_base(__VA_ARGS__)
#endif

#define LAPACK_zgeev_base LAPACK_GLOBAL(zgeev,ZGEEV)
void LAPACK_zgeev_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* W,
    lapack_complex_double* VL, lapack_int const* ldvl,
    lapack_complex_double* VR, lapack_int const* ldvr,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgeev(...) LAPACK_zgeev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgeev(...) LAPACK_zgeev_base(__VA_ARGS__)
#endif

#define LAPACK_cgeevx_base LAPACK_GLOBAL(cgeevx,CGEEVX)
void LAPACK_cgeevx_base(
    char const* balanc, char const* jobvl, char const* jobvr, char const* sense,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* W,
    lapack_complex_float* VL, lapack_int const* ldvl,
    lapack_complex_float* VR, lapack_int const* ldvr, lapack_int* ilo, lapack_int* ihi,
    float* scale,
    float* abnrm,
    float* rconde,
    float* rcondv,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgeevx(...) LAPACK_cgeevx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_cgeevx(...) LAPACK_cgeevx_base(__VA_ARGS__)
#endif

#define LAPACK_dgeevx_base LAPACK_GLOBAL(dgeevx,DGEEVX)
void LAPACK_dgeevx_base(
    char const* balanc, char const* jobvl, char const* jobvr, char const* sense,
    lapack_int const* n,
    double* A, lapack_int const* lda,
    double* WR,
    double* WI,
    double* VL, lapack_int const* ldvl,
    double* VR, lapack_int const* ldvr, lapack_int* ilo, lapack_int* ihi,
    double* scale,
    double* abnrm,
    double* rconde,
    double* rcondv,
    double* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgeevx(...) LAPACK_dgeevx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_dgeevx(...) LAPACK_dgeevx_base(__VA_ARGS__)
#endif

#define LAPACK_sgeevx_base LAPACK_GLOBAL(sgeevx,SGEEVX)
void LAPACK_sgeevx_base(
    char const* balanc, char const* jobvl, char const* jobvr, char const* sense,
    lapack_int const* n,
    float* A, lapack_int const* lda,
    float* WR,
    float* WI,
    float* VL, lapack_int const* ldvl,
    float* VR, lapack_int const* ldvr, lapack_int* ilo, lapack_int* ihi,
    float* scale,
    float* abnrm,
    float* rconde,
    float* rcondv,
    float* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgeevx(...) LAPACK_sgeevx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_sgeevx(...) LAPACK_sgeevx_base(__VA_ARGS__)
#endif

#define LAPACK_zgeevx_base LAPACK_GLOBAL(zgeevx,ZGEEVX)
void LAPACK_zgeevx_base(
    char const* balanc, char const* jobvl, char const* jobvr, char const* sense,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* W,
    lapack_complex_double* VL, lapack_int const* ldvl,
    lapack_complex_double* VR, lapack_int const* ldvr, lapack_int* ilo, lapack_int* ihi,
    double* scale,
    double* abnrm,
    double* rconde,
    double* rcondv,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgeevx(...) LAPACK_zgeevx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_zgeevx(...) LAPACK_zgeevx_base(__VA_ARGS__)
#endif

#define LAPACK_cgehrd LAPACK_GLOBAL(cgehrd,CGEHRD)
void LAPACK_cgehrd(
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* tau,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgehrd LAPACK_GLOBAL(dgehrd,DGEHRD)
void LAPACK_dgehrd(
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    double* A, lapack_int const* lda,
    double* tau,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgehrd LAPACK_GLOBAL(sgehrd,SGEHRD)
void LAPACK_sgehrd(
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    float* A, lapack_int const* lda,
    float* tau,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgehrd LAPACK_GLOBAL(zgehrd,ZGEHRD)
void LAPACK_zgehrd(
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* tau,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cgejsv_base LAPACK_GLOBAL(cgejsv,CGEJSV)
void LAPACK_cgejsv_base(
    char const* joba, char const* jobu, char const* jobv, char const* jobr, char const* jobt, char const* jobp,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* SVA,
    lapack_complex_float* U, lapack_int const* ldu,
    lapack_complex_float* V, lapack_int const* ldv,
    lapack_complex_float* cwork, lapack_int const* lwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgejsv(...) LAPACK_cgejsv_base(__VA_ARGS__, 1, 1, 1, 1, 1, 1)
#else
    #define LAPACK_cgejsv(...) LAPACK_cgejsv_base(__VA_ARGS__)
#endif

#define LAPACK_dgejsv_base LAPACK_GLOBAL(dgejsv,DGEJSV)
void LAPACK_dgejsv_base(
    char const* joba, char const* jobu, char const* jobv, char const* jobr, char const* jobt, char const* jobp,
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* SVA,
    double* U, lapack_int const* ldu,
    double* V, lapack_int const* ldv,
    double* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgejsv(...) LAPACK_dgejsv_base(__VA_ARGS__, 1, 1, 1, 1, 1, 1)
#else
    #define LAPACK_dgejsv(...) LAPACK_dgejsv_base(__VA_ARGS__)
#endif

#define LAPACK_sgejsv_base LAPACK_GLOBAL(sgejsv,SGEJSV)
void LAPACK_sgejsv_base(
    char const* joba, char const* jobu, char const* jobv, char const* jobr, char const* jobt, char const* jobp,
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* SVA,
    float* U, lapack_int const* ldu,
    float* V, lapack_int const* ldv,
    float* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgejsv(...) LAPACK_sgejsv_base(__VA_ARGS__, 1, 1, 1, 1, 1, 1)
#else
    #define LAPACK_sgejsv(...) LAPACK_sgejsv_base(__VA_ARGS__)
#endif

#define LAPACK_zgejsv_base LAPACK_GLOBAL(zgejsv,ZGEJSV)
void LAPACK_zgejsv_base(
    char const* joba, char const* jobu, char const* jobv, char const* jobr, char const* jobt, char const* jobp,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* SVA,
    lapack_complex_double* U, lapack_int const* ldu,
    lapack_complex_double* V, lapack_int const* ldv,
    lapack_complex_double* cwork, lapack_int const* lwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgejsv(...) LAPACK_zgejsv_base(__VA_ARGS__, 1, 1, 1, 1, 1, 1)
#else
    #define LAPACK_zgejsv(...) LAPACK_zgejsv_base(__VA_ARGS__)
#endif

#define LAPACK_cgelq LAPACK_GLOBAL(cgelq,CGELQ)
void LAPACK_cgelq(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* T, lapack_int const* tsize,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgelq LAPACK_GLOBAL(dgelq,DGELQ)
void LAPACK_dgelq(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* T, lapack_int const* tsize,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgelq LAPACK_GLOBAL(sgelq,SGELQ)
void LAPACK_sgelq(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* T, lapack_int const* tsize,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgelq LAPACK_GLOBAL(zgelq,ZGELQ)
void LAPACK_zgelq(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* T, lapack_int const* tsize,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cgelq2 LAPACK_GLOBAL(cgelq2,CGELQ2)
void LAPACK_cgelq2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* tau,
    lapack_complex_float* work,
    lapack_int* info );

#define LAPACK_dgelq2 LAPACK_GLOBAL(dgelq2,DGELQ2)
void LAPACK_dgelq2(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* tau,
    double* work,
    lapack_int* info );

#define LAPACK_sgelq2 LAPACK_GLOBAL(sgelq2,SGELQ2)
void LAPACK_sgelq2(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* tau,
    float* work,
    lapack_int* info );

#define LAPACK_zgelq2 LAPACK_GLOBAL(zgelq2,ZGELQ2)
void LAPACK_zgelq2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* tau,
    lapack_complex_double* work,
    lapack_int* info );

#define LAPACK_cgelqf LAPACK_GLOBAL(cgelqf,CGELQF)
void LAPACK_cgelqf(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* tau,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgelqf LAPACK_GLOBAL(dgelqf,DGELQF)
void LAPACK_dgelqf(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* tau,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgelqf LAPACK_GLOBAL(sgelqf,SGELQF)
void LAPACK_sgelqf(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* tau,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgelqf LAPACK_GLOBAL(zgelqf,ZGELQF)
void LAPACK_zgelqf(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* tau,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cgels_base LAPACK_GLOBAL(cgels,CGELS)
void LAPACK_cgels_base(
    char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgels(...) LAPACK_cgels_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgels(...) LAPACK_cgels_base(__VA_ARGS__)
#endif

#define LAPACK_dgels_base LAPACK_GLOBAL(dgels,DGELS)
void LAPACK_dgels_base(
    char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgels(...) LAPACK_dgels_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgels(...) LAPACK_dgels_base(__VA_ARGS__)
#endif

#define LAPACK_sgels_base LAPACK_GLOBAL(sgels,SGELS)
void LAPACK_sgels_base(
    char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgels(...) LAPACK_sgels_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgels(...) LAPACK_sgels_base(__VA_ARGS__)
#endif

#define LAPACK_zgels_base LAPACK_GLOBAL(zgels,ZGELS)
void LAPACK_zgels_base(
    char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgels(...) LAPACK_zgels_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgels(...) LAPACK_zgels_base(__VA_ARGS__)
#endif

#define LAPACK_cgelsd LAPACK_GLOBAL(cgelsd,CGELSD)
void LAPACK_cgelsd(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    float* S,
    float const* rcond, lapack_int* rank,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* iwork,
    lapack_int* info );

#define LAPACK_dgelsd LAPACK_GLOBAL(dgelsd,DGELSD)
void LAPACK_dgelsd(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* S,
    double const* rcond, lapack_int* rank,
    double* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info );

#define LAPACK_sgelsd LAPACK_GLOBAL(sgelsd,SGELSD)
void LAPACK_sgelsd(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* S,
    float const* rcond, lapack_int* rank,
    float* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info );

#define LAPACK_zgelsd LAPACK_GLOBAL(zgelsd,ZGELSD)
void LAPACK_zgelsd(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    double* S,
    double const* rcond, lapack_int* rank,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* iwork,
    lapack_int* info );

#define LAPACK_cgelss LAPACK_GLOBAL(cgelss,CGELSS)
void LAPACK_cgelss(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    float* S,
    float const* rcond, lapack_int* rank,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info );

#define LAPACK_dgelss LAPACK_GLOBAL(dgelss,DGELSS)
void LAPACK_dgelss(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* S,
    double const* rcond, lapack_int* rank,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgelss LAPACK_GLOBAL(sgelss,SGELSS)
void LAPACK_sgelss(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* S,
    float const* rcond, lapack_int* rank,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgelss LAPACK_GLOBAL(zgelss,ZGELSS)
void LAPACK_zgelss(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    double* S,
    double const* rcond, lapack_int* rank,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info );

#define LAPACK_cgelsy LAPACK_GLOBAL(cgelsy,CGELSY)
void LAPACK_cgelsy(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb, lapack_int* JPVT,
    float const* rcond, lapack_int* rank,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info );

#define LAPACK_dgelsy LAPACK_GLOBAL(dgelsy,DGELSY)
void LAPACK_dgelsy(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb, lapack_int* JPVT,
    double const* rcond, lapack_int* rank,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgelsy LAPACK_GLOBAL(sgelsy,SGELSY)
void LAPACK_sgelsy(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb, lapack_int* JPVT,
    float const* rcond, lapack_int* rank,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgelsy LAPACK_GLOBAL(zgelsy,ZGELSY)
void LAPACK_zgelsy(
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb, lapack_int* JPVT,
    double const* rcond, lapack_int* rank,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info );

#define LAPACK_cgemlq_base LAPACK_GLOBAL(cgemlq,CGEMLQ)
void LAPACK_cgemlq_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k,
    lapack_complex_float const* A, lapack_int const* lda,
    lapack_complex_float const* T, lapack_int const* tsize,
    lapack_complex_float* C, lapack_int const* ldc,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgemlq(...) LAPACK_cgemlq_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgemlq(...) LAPACK_cgemlq_base(__VA_ARGS__)
#endif

#define LAPACK_dgemlq_base LAPACK_GLOBAL(dgemlq,DGEMLQ)
void LAPACK_dgemlq_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k,
    double const* A, lapack_int const* lda,
    double const* T, lapack_int const* tsize,
    double* C, lapack_int const* ldc,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgemlq(...) LAPACK_dgemlq_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgemlq(...) LAPACK_dgemlq_base(__VA_ARGS__)
#endif

#define LAPACK_sgemlq_base LAPACK_GLOBAL(sgemlq,SGEMLQ)
void LAPACK_sgemlq_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k,
    float const* A, lapack_int const* lda,
    float const* T, lapack_int const* tsize,
    float* C, lapack_int const* ldc,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgemlq(...) LAPACK_sgemlq_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgemlq(...) LAPACK_sgemlq_base(__VA_ARGS__)
#endif

#define LAPACK_zgemlq_base LAPACK_GLOBAL(zgemlq,ZGEMLQ)
void LAPACK_zgemlq_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k,
    lapack_complex_double const* A, lapack_int const* lda,
    lapack_complex_double const* T, lapack_int const* tsize,
    lapack_complex_double* C, lapack_int const* ldc,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgemlq(...) LAPACK_zgemlq_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgemlq(...) LAPACK_zgemlq_base(__VA_ARGS__)
#endif

#define LAPACK_cgemqr_base LAPACK_GLOBAL(cgemqr,CGEMQR)
void LAPACK_cgemqr_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k,
    lapack_complex_float const* A, lapack_int const* lda,
    lapack_complex_float const* T, lapack_int const* tsize,
    lapack_complex_float* C, lapack_int const* ldc,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgemqr(...) LAPACK_cgemqr_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgemqr(...) LAPACK_cgemqr_base(__VA_ARGS__)
#endif

#define LAPACK_dgemqr_base LAPACK_GLOBAL(dgemqr,DGEMQR)
void LAPACK_dgemqr_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k,
    double const* A, lapack_int const* lda,
    double const* T, lapack_int const* tsize,
    double* C, lapack_int const* ldc,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgemqr(...) LAPACK_dgemqr_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgemqr(...) LAPACK_dgemqr_base(__VA_ARGS__)
#endif

#define LAPACK_sgemqr_base LAPACK_GLOBAL(sgemqr,SGEMQR)
void LAPACK_sgemqr_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k,
    float const* A, lapack_int const* lda,
    float const* T, lapack_int const* tsize,
    float* C, lapack_int const* ldc,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgemqr(...) LAPACK_sgemqr_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgemqr(...) LAPACK_sgemqr_base(__VA_ARGS__)
#endif

#define LAPACK_zgemqr_base LAPACK_GLOBAL(zgemqr,ZGEMQR)
void LAPACK_zgemqr_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k,
    lapack_complex_double const* A, lapack_int const* lda,
    lapack_complex_double const* T, lapack_int const* tsize,
    lapack_complex_double* C, lapack_int const* ldc,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgemqr(...) LAPACK_zgemqr_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgemqr(...) LAPACK_zgemqr_base(__VA_ARGS__)
#endif

#define LAPACK_cgemqrt_base LAPACK_GLOBAL(cgemqrt,CGEMQRT)
void LAPACK_cgemqrt_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k, lapack_int const* nb,
    lapack_complex_float const* V, lapack_int const* ldv,
    lapack_complex_float const* T, lapack_int const* ldt,
    lapack_complex_float* C, lapack_int const* ldc,
    lapack_complex_float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgemqrt(...) LAPACK_cgemqrt_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgemqrt(...) LAPACK_cgemqrt_base(__VA_ARGS__)
#endif

#define LAPACK_dgemqrt_base LAPACK_GLOBAL(dgemqrt,DGEMQRT)
void LAPACK_dgemqrt_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k, lapack_int const* nb,
    double const* V, lapack_int const* ldv,
    double const* T, lapack_int const* ldt,
    double* C, lapack_int const* ldc,
    double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgemqrt(...) LAPACK_dgemqrt_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgemqrt(...) LAPACK_dgemqrt_base(__VA_ARGS__)
#endif

#define LAPACK_sgemqrt_base LAPACK_GLOBAL(sgemqrt,SGEMQRT)
void LAPACK_sgemqrt_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k, lapack_int const* nb,
    float const* V, lapack_int const* ldv,
    float const* T, lapack_int const* ldt,
    float* C, lapack_int const* ldc,
    float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgemqrt(...) LAPACK_sgemqrt_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgemqrt(...) LAPACK_sgemqrt_base(__VA_ARGS__)
#endif

#define LAPACK_zgemqrt_base LAPACK_GLOBAL(zgemqrt,ZGEMQRT)
void LAPACK_zgemqrt_base(
    char const* side, char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* k, lapack_int const* nb,
    lapack_complex_double const* V, lapack_int const* ldv,
    lapack_complex_double const* T, lapack_int const* ldt,
    lapack_complex_double* C, lapack_int const* ldc,
    lapack_complex_double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgemqrt(...) LAPACK_zgemqrt_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgemqrt(...) LAPACK_zgemqrt_base(__VA_ARGS__)
#endif

#define LAPACK_cgeql2 LAPACK_GLOBAL(cgeql2,CGEQL2)
void LAPACK_cgeql2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* tau,
    lapack_complex_float* work,
    lapack_int* info );

#define LAPACK_dgeql2 LAPACK_GLOBAL(dgeql2,DGEQL2)
void LAPACK_dgeql2(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* tau,
    double* work,
    lapack_int* info );

#define LAPACK_sgeql2 LAPACK_GLOBAL(sgeql2,SGEQL2)
void LAPACK_sgeql2(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* tau,
    float* work,
    lapack_int* info );

#define LAPACK_zgeql2 LAPACK_GLOBAL(zgeql2,ZGEQL2)
void LAPACK_zgeql2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* tau,
    lapack_complex_double* work,
    lapack_int* info );

#define LAPACK_cgeqlf LAPACK_GLOBAL(cgeqlf,CGEQLF)
void LAPACK_cgeqlf(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* tau,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgeqlf LAPACK_GLOBAL(dgeqlf,DGEQLF)
void LAPACK_dgeqlf(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* tau,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgeqlf LAPACK_GLOBAL(sgeqlf,SGEQLF)
void LAPACK_sgeqlf(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* tau,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgeqlf LAPACK_GLOBAL(zgeqlf,ZGEQLF)
void LAPACK_zgeqlf(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* tau,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgeqpf LAPACK_GLOBAL(sgeqpf,SGEQPF)
void LAPACK_sgeqpf( lapack_int* m, lapack_int* n, float* a, lapack_int* lda,
                    lapack_int* jpvt, float* tau, float* work,
                    lapack_int *info );

#define LAPACK_dgeqpf LAPACK_GLOBAL(dgeqpf,DGEQPF)
void LAPACK_dgeqpf( lapack_int* m, lapack_int* n, double* a, lapack_int* lda,
                    lapack_int* jpvt, double* tau, double* work,
                    lapack_int *info );

#define LAPACK_cgeqpf LAPACK_GLOBAL(cgeqpf,CGEQPF)
void LAPACK_cgeqpf( lapack_int* m, lapack_int* n, lapack_complex_float* a,
                    lapack_int* lda, lapack_int* jpvt,
                    lapack_complex_float* tau, lapack_complex_float* work,
                    float* rwork, lapack_int *info );

#define LAPACK_zgeqpf LAPACK_GLOBAL(zgeqpf,ZGEQPF)
void LAPACK_zgeqpf( lapack_int* m, lapack_int* n, lapack_complex_double* a,
                    lapack_int* lda, lapack_int* jpvt,
                    lapack_complex_double* tau, lapack_complex_double* work,
                    double* rwork, lapack_int *info );

#define LAPACK_cgeqp3 LAPACK_GLOBAL(cgeqp3,CGEQP3)
void LAPACK_cgeqp3(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* JPVT,
    lapack_complex_float* tau,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info );

#define LAPACK_dgeqp3 LAPACK_GLOBAL(dgeqp3,DGEQP3)
void LAPACK_dgeqp3(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda, lapack_int* JPVT,
    double* tau,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgeqp3 LAPACK_GLOBAL(sgeqp3,SGEQP3)
void LAPACK_sgeqp3(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda, lapack_int* JPVT,
    float* tau,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgeqp3 LAPACK_GLOBAL(zgeqp3,ZGEQP3)
void LAPACK_zgeqp3(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* JPVT,
    lapack_complex_double* tau,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info );

#define LAPACK_cgeqr LAPACK_GLOBAL(cgeqr,CGEQR)
void LAPACK_cgeqr(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* T, lapack_int const* tsize,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgeqr LAPACK_GLOBAL(dgeqr,DGEQR)
void LAPACK_dgeqr(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* T, lapack_int const* tsize,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgeqr LAPACK_GLOBAL(sgeqr,SGEQR)
void LAPACK_sgeqr(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* T, lapack_int const* tsize,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgeqr LAPACK_GLOBAL(zgeqr,ZGEQR)
void LAPACK_zgeqr(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* T, lapack_int const* tsize,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cgeqr2 LAPACK_GLOBAL(cgeqr2,CGEQR2)
void LAPACK_cgeqr2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* tau,
    lapack_complex_float* work,
    lapack_int* info );

#define LAPACK_dgeqr2 LAPACK_GLOBAL(dgeqr2,DGEQR2)
void LAPACK_dgeqr2(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* tau,
    double* work,
    lapack_int* info );

#define LAPACK_sgeqr2 LAPACK_GLOBAL(sgeqr2,SGEQR2)
void LAPACK_sgeqr2(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* tau,
    float* work,
    lapack_int* info );

#define LAPACK_zgeqr2 LAPACK_GLOBAL(zgeqr2,ZGEQR2)
void LAPACK_zgeqr2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* tau,
    lapack_complex_double* work,
    lapack_int* info );

#define LAPACK_cgeqrf LAPACK_GLOBAL(cgeqrf,CGEQRF)
void LAPACK_cgeqrf(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* tau,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgeqrf LAPACK_GLOBAL(dgeqrf,DGEQRF)
void LAPACK_dgeqrf(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* tau,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgeqrf LAPACK_GLOBAL(sgeqrf,SGEQRF)
void LAPACK_sgeqrf(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* tau,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgeqrf LAPACK_GLOBAL(zgeqrf,ZGEQRF)
void LAPACK_zgeqrf(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* tau,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cgeqrfp LAPACK_GLOBAL(cgeqrfp,CGEQRFP)
void LAPACK_cgeqrfp(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* tau,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgeqrfp LAPACK_GLOBAL(dgeqrfp,DGEQRFP)
void LAPACK_dgeqrfp(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* tau,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgeqrfp LAPACK_GLOBAL(sgeqrfp,SGEQRFP)
void LAPACK_sgeqrfp(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* tau,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgeqrfp LAPACK_GLOBAL(zgeqrfp,ZGEQRFP)
void LAPACK_zgeqrfp(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* tau,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cgeqrt LAPACK_GLOBAL(cgeqrt,CGEQRT)
void LAPACK_cgeqrt(
    lapack_int const* m, lapack_int const* n, lapack_int const* nb,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* T, lapack_int const* ldt,
    lapack_complex_float* work,
    lapack_int* info );

#define LAPACK_dgeqrt LAPACK_GLOBAL(dgeqrt,DGEQRT)
void LAPACK_dgeqrt(
    lapack_int const* m, lapack_int const* n, lapack_int const* nb,
    double* A, lapack_int const* lda,
    double* T, lapack_int const* ldt,
    double* work,
    lapack_int* info );

#define LAPACK_sgeqrt LAPACK_GLOBAL(sgeqrt,SGEQRT)
void LAPACK_sgeqrt(
    lapack_int const* m, lapack_int const* n, lapack_int const* nb,
    float* A, lapack_int const* lda,
    float* T, lapack_int const* ldt,
    float* work,
    lapack_int* info );

#define LAPACK_zgeqrt LAPACK_GLOBAL(zgeqrt,ZGEQRT)
void LAPACK_zgeqrt(
    lapack_int const* m, lapack_int const* n, lapack_int const* nb,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* T, lapack_int const* ldt,
    lapack_complex_double* work,
    lapack_int* info );

#define LAPACK_cgeqrt2 LAPACK_GLOBAL(cgeqrt2,CGEQRT2)
void LAPACK_cgeqrt2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* T, lapack_int const* ldt,
    lapack_int* info );

#define LAPACK_dgeqrt2 LAPACK_GLOBAL(dgeqrt2,DGEQRT2)
void LAPACK_dgeqrt2(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* T, lapack_int const* ldt,
    lapack_int* info );

#define LAPACK_sgeqrt2 LAPACK_GLOBAL(sgeqrt2,SGEQRT2)
void LAPACK_sgeqrt2(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* T, lapack_int const* ldt,
    lapack_int* info );

#define LAPACK_zgeqrt2 LAPACK_GLOBAL(zgeqrt2,ZGEQRT2)
void LAPACK_zgeqrt2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* T, lapack_int const* ldt,
    lapack_int* info );

#define LAPACK_cgeqrt3 LAPACK_GLOBAL(cgeqrt3,CGEQRT3)
void LAPACK_cgeqrt3(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* T, lapack_int const* ldt,
    lapack_int* info );

#define LAPACK_dgeqrt3 LAPACK_GLOBAL(dgeqrt3,DGEQRT3)
void LAPACK_dgeqrt3(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* T, lapack_int const* ldt,
    lapack_int* info );

#define LAPACK_sgeqrt3 LAPACK_GLOBAL(sgeqrt3,SGEQRT3)
void LAPACK_sgeqrt3(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* T, lapack_int const* ldt,
    lapack_int* info );

#define LAPACK_zgeqrt3 LAPACK_GLOBAL(zgeqrt3,ZGEQRT3)
void LAPACK_zgeqrt3(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* T, lapack_int const* ldt,
    lapack_int* info );

#define LAPACK_cgerfs_base LAPACK_GLOBAL(cgerfs,CGERFS)
void LAPACK_cgerfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float const* A, lapack_int const* lda,
    lapack_complex_float const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    lapack_complex_float const* B, lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* ferr,
    float* berr,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgerfs(...) LAPACK_cgerfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgerfs(...) LAPACK_cgerfs_base(__VA_ARGS__)
#endif

#define LAPACK_dgerfs_base LAPACK_GLOBAL(dgerfs,DGERFS)
void LAPACK_dgerfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    double const* A, lapack_int const* lda,
    double const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    double const* B, lapack_int const* ldb,
    double* X, lapack_int const* ldx,
    double* ferr,
    double* berr,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgerfs(...) LAPACK_dgerfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgerfs(...) LAPACK_dgerfs_base(__VA_ARGS__)
#endif

#define LAPACK_sgerfs_base LAPACK_GLOBAL(sgerfs,SGERFS)
void LAPACK_sgerfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    float const* A, lapack_int const* lda,
    float const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    float const* B, lapack_int const* ldb,
    float* X, lapack_int const* ldx,
    float* ferr,
    float* berr,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgerfs(...) LAPACK_sgerfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgerfs(...) LAPACK_sgerfs_base(__VA_ARGS__)
#endif

#define LAPACK_zgerfs_base LAPACK_GLOBAL(zgerfs,ZGERFS)
void LAPACK_zgerfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double const* A, lapack_int const* lda,
    lapack_complex_double const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    lapack_complex_double const* B, lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* ferr,
    double* berr,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgerfs(...) LAPACK_zgerfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgerfs(...) LAPACK_zgerfs_base(__VA_ARGS__)
#endif

#define LAPACK_cgerfsx_base LAPACK_GLOBAL(cgerfsx,CGERFSX)
void LAPACK_cgerfsx_base(
    char const* trans, char const* equed,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float const* A, lapack_int const* lda,
    lapack_complex_float const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    float const* R,
    float const* C,
    lapack_complex_float const* B, lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* rcond,
    float* berr, lapack_int const* n_err_bnds,
    float* err_bnds_norm,
    float* err_bnds_comp, lapack_int const* nparams,
    float* params,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgerfsx(...) LAPACK_cgerfsx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgerfsx(...) LAPACK_cgerfsx_base(__VA_ARGS__)
#endif

#define LAPACK_dgerfsx_base LAPACK_GLOBAL(dgerfsx,DGERFSX)
void LAPACK_dgerfsx_base(
    char const* trans, char const* equed,
    lapack_int const* n, lapack_int const* nrhs,
    double const* A, lapack_int const* lda,
    double const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    double const* R,
    double const* C,
    double const* B, lapack_int const* ldb,
    double* X, lapack_int const* ldx,
    double* rcond,
    double* berr, lapack_int const* n_err_bnds,
    double* err_bnds_norm,
    double* err_bnds_comp, lapack_int const* nparams,
    double* params,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgerfsx(...) LAPACK_dgerfsx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgerfsx(...) LAPACK_dgerfsx_base(__VA_ARGS__)
#endif

#define LAPACK_sgerfsx_base LAPACK_GLOBAL(sgerfsx,SGERFSX)
void LAPACK_sgerfsx_base(
    char const* trans, char const* equed,
    lapack_int const* n, lapack_int const* nrhs,
    float const* A, lapack_int const* lda,
    float const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    float const* R,
    float const* C,
    float const* B, lapack_int const* ldb,
    float* X, lapack_int const* ldx,
    float* rcond,
    float* berr, lapack_int const* n_err_bnds,
    float* err_bnds_norm,
    float* err_bnds_comp, lapack_int const* nparams,
    float* params,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgerfsx(...) LAPACK_sgerfsx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgerfsx(...) LAPACK_sgerfsx_base(__VA_ARGS__)
#endif

#define LAPACK_zgerfsx_base LAPACK_GLOBAL(zgerfsx,ZGERFSX)
void LAPACK_zgerfsx_base(
    char const* trans, char const* equed,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double const* A, lapack_int const* lda,
    lapack_complex_double const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    double const* R,
    double const* C,
    lapack_complex_double const* B, lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* rcond,
    double* berr, lapack_int const* n_err_bnds,
    double* err_bnds_norm,
    double* err_bnds_comp, lapack_int const* nparams,
    double* params,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgerfsx(...) LAPACK_zgerfsx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgerfsx(...) LAPACK_zgerfsx_base(__VA_ARGS__)
#endif

#define LAPACK_cgerq2 LAPACK_GLOBAL(cgerq2,CGERQ2)
void LAPACK_cgerq2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* tau,
    lapack_complex_float* work,
    lapack_int* info );

#define LAPACK_dgerq2 LAPACK_GLOBAL(dgerq2,DGERQ2)
void LAPACK_dgerq2(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* tau,
    double* work,
    lapack_int* info );

#define LAPACK_sgerq2 LAPACK_GLOBAL(sgerq2,SGERQ2)
void LAPACK_sgerq2(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* tau,
    float* work,
    lapack_int* info );

#define LAPACK_zgerq2 LAPACK_GLOBAL(zgerq2,ZGERQ2)
void LAPACK_zgerq2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* tau,
    lapack_complex_double* work,
    lapack_int* info );

#define LAPACK_cgerqf LAPACK_GLOBAL(cgerqf,CGERQF)
void LAPACK_cgerqf(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* tau,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgerqf LAPACK_GLOBAL(dgerqf,DGERQF)
void LAPACK_dgerqf(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* tau,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgerqf LAPACK_GLOBAL(sgerqf,SGERQF)
void LAPACK_sgerqf(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* tau,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgerqf LAPACK_GLOBAL(zgerqf,ZGERQF)
void LAPACK_zgerqf(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* tau,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cgesdd_base LAPACK_GLOBAL(cgesdd,CGESDD)
void LAPACK_cgesdd_base(
    char const* jobz,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* S,
    lapack_complex_float* U, lapack_int const* ldu,
    lapack_complex_float* VT, lapack_int const* ldvt,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgesdd(...) LAPACK_cgesdd_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgesdd(...) LAPACK_cgesdd_base(__VA_ARGS__)
#endif

#define LAPACK_dgesdd_base LAPACK_GLOBAL(dgesdd,DGESDD)
void LAPACK_dgesdd_base(
    char const* jobz,
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* S,
    double* U, lapack_int const* ldu,
    double* VT, lapack_int const* ldvt,
    double* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgesdd(...) LAPACK_dgesdd_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgesdd(...) LAPACK_dgesdd_base(__VA_ARGS__)
#endif

#define LAPACK_sgesdd_base LAPACK_GLOBAL(sgesdd,SGESDD)
void LAPACK_sgesdd_base(
    char const* jobz,
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* S,
    float* U, lapack_int const* ldu,
    float* VT, lapack_int const* ldvt,
    float* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgesdd(...) LAPACK_sgesdd_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgesdd(...) LAPACK_sgesdd_base(__VA_ARGS__)
#endif

#define LAPACK_zgesdd_base LAPACK_GLOBAL(zgesdd,ZGESDD)
void LAPACK_zgesdd_base(
    char const* jobz,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* S,
    lapack_complex_double* U, lapack_int const* ldu,
    lapack_complex_double* VT, lapack_int const* ldvt,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgesdd(...) LAPACK_zgesdd_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgesdd(...) LAPACK_zgesdd_base(__VA_ARGS__)
#endif

#define LAPACK_cgesv LAPACK_GLOBAL(cgesv,CGESV)
void LAPACK_cgesv(
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_dgesv LAPACK_GLOBAL(dgesv,DGESV)
void LAPACK_dgesv(
    lapack_int const* n, lapack_int const* nrhs,
    double* A, lapack_int const* lda, lapack_int* ipiv,
    double* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_sgesv LAPACK_GLOBAL(sgesv,SGESV)
void LAPACK_sgesv(
    lapack_int const* n, lapack_int const* nrhs,
    float* A, lapack_int const* lda, lapack_int* ipiv,
    float* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_zgesv LAPACK_GLOBAL(zgesv,ZGESV)
void LAPACK_zgesv(
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_dsgesv LAPACK_GLOBAL(dsgesv,DSGESV)
void LAPACK_dsgesv(
    lapack_int const* n, lapack_int const* nrhs,
    double* A, lapack_int const* lda, lapack_int* ipiv,
    double const* B, lapack_int const* ldb,
    double* X, lapack_int const* ldx,
    double* work,
    float* swork, lapack_int* iter,
    lapack_int* info );

#define LAPACK_zcgesv LAPACK_GLOBAL(zcgesv,ZCGESV)
void LAPACK_zcgesv(
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_double const* B, lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    lapack_complex_double* work,
    lapack_complex_float* swork,
    double* rwork, lapack_int* iter,
    lapack_int* info );

#define LAPACK_cgesvd_base LAPACK_GLOBAL(cgesvd,CGESVD)
void LAPACK_cgesvd_base(
    char const* jobu, char const* jobvt,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* S,
    lapack_complex_float* U, lapack_int const* ldu,
    lapack_complex_float* VT, lapack_int const* ldvt,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgesvd(...) LAPACK_cgesvd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgesvd(...) LAPACK_cgesvd_base(__VA_ARGS__)
#endif

#define LAPACK_dgesvd_base LAPACK_GLOBAL(dgesvd,DGESVD)
void LAPACK_dgesvd_base(
    char const* jobu, char const* jobvt,
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* S,
    double* U, lapack_int const* ldu,
    double* VT, lapack_int const* ldvt,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgesvd(...) LAPACK_dgesvd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgesvd(...) LAPACK_dgesvd_base(__VA_ARGS__)
#endif

#define LAPACK_sgesvd_base LAPACK_GLOBAL(sgesvd,SGESVD)
void LAPACK_sgesvd_base(
    char const* jobu, char const* jobvt,
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* S,
    float* U, lapack_int const* ldu,
    float* VT, lapack_int const* ldvt,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgesvd(...) LAPACK_sgesvd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgesvd(...) LAPACK_sgesvd_base(__VA_ARGS__)
#endif

#define LAPACK_zgesvd_base LAPACK_GLOBAL(zgesvd,ZGESVD)
void LAPACK_zgesvd_base(
    char const* jobu, char const* jobvt,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* S,
    lapack_complex_double* U, lapack_int const* ldu,
    lapack_complex_double* VT, lapack_int const* ldvt,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgesvd(...) LAPACK_zgesvd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgesvd(...) LAPACK_zgesvd_base(__VA_ARGS__)
#endif

#define LAPACK_cgesvdq_base LAPACK_GLOBAL(cgesvdq,CGESVDQ)
void LAPACK_cgesvdq_base(
    char const* joba, char const* jobp, char const* jobr, char const* jobu, char const* jobv,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* S,
    lapack_complex_float* U, lapack_int const* ldu,
    lapack_complex_float* V, lapack_int const* ldv, lapack_int* numrank,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_complex_float* cwork, lapack_int* lcwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgesvdq(...) LAPACK_cgesvdq_base(__VA_ARGS__, 1, 1, 1, 1, 1)
#else
    #define LAPACK_cgesvdq(...) LAPACK_cgesvdq_base(__VA_ARGS__)
#endif

#define LAPACK_dgesvdq_base LAPACK_GLOBAL(dgesvdq,DGESVDQ)
void LAPACK_dgesvdq_base(
    char const* joba, char const* jobp, char const* jobr, char const* jobu, char const* jobv,
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* S,
    double* U, lapack_int const* ldu,
    double* V, lapack_int const* ldv, lapack_int* numrank,
    lapack_int* iwork, lapack_int const* liwork,
    double* work, lapack_int* lwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgesvdq(...) LAPACK_dgesvdq_base(__VA_ARGS__, 1, 1, 1, 1, 1)
#else
    #define LAPACK_dgesvdq(...) LAPACK_dgesvdq_base(__VA_ARGS__)
#endif

#define LAPACK_sgesvdq_base LAPACK_GLOBAL(sgesvdq,SGESVDQ)
void LAPACK_sgesvdq_base(
    char const* joba, char const* jobp, char const* jobr, char const* jobu, char const* jobv,
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* S,
    float* U, lapack_int const* ldu,
    float* V, lapack_int const* ldv, lapack_int* numrank,
    lapack_int* iwork, lapack_int const* liwork,
    float* work, lapack_int* lwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgesvdq(...) LAPACK_sgesvdq_base(__VA_ARGS__, 1, 1, 1, 1, 1)
#else
    #define LAPACK_sgesvdq(...) LAPACK_sgesvdq_base(__VA_ARGS__)
#endif

#define LAPACK_zgesvdq_base LAPACK_GLOBAL(zgesvdq,ZGESVDQ)
void LAPACK_zgesvdq_base(
    char const* joba, char const* jobp, char const* jobr, char const* jobu, char const* jobv,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* S,
    lapack_complex_double* U, lapack_int const* ldu,
    lapack_complex_double* V, lapack_int const* ldv, lapack_int* numrank,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_complex_double* cwork, lapack_int* lcwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgesvdq(...) LAPACK_zgesvdq_base(__VA_ARGS__, 1, 1, 1, 1, 1)
#else
    #define LAPACK_zgesvdq(...) LAPACK_zgesvdq_base(__VA_ARGS__)
#endif

#define LAPACK_cgesvdx_base LAPACK_GLOBAL(cgesvdx,CGESVDX)
void LAPACK_cgesvdx_base(
    char const* jobu, char const* jobvt, char const* range,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float const* vl,
    float const* vu, lapack_int const* il, lapack_int const* iu, lapack_int* ns,
    float* S,
    lapack_complex_float* U, lapack_int const* ldu,
    lapack_complex_float* VT, lapack_int const* ldvt,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgesvdx(...) LAPACK_cgesvdx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cgesvdx(...) LAPACK_cgesvdx_base(__VA_ARGS__)
#endif


#define LAPACK_dgesvdx_base LAPACK_GLOBAL(dgesvdx,DGESVDX)
void LAPACK_dgesvdx_base(
    char const* jobu, char const* jobvt, char const* range,
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double const* vl,
    double const* vu, lapack_int const* il, lapack_int const* iu, lapack_int* ns,
    double* S,
    double* U, lapack_int const* ldu,
    double* VT, lapack_int const* ldvt,
    double* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgesvdx(...) LAPACK_dgesvdx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dgesvdx(...) LAPACK_dgesvdx_base(__VA_ARGS__)
#endif

#define LAPACK_sgesvdx_base LAPACK_GLOBAL(sgesvdx,SGESVDX)
void LAPACK_sgesvdx_base(
    char const* jobu, char const* jobvt, char const* range,
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float const* vl,
    float const* vu, lapack_int const* il, lapack_int const* iu, lapack_int* ns,
    float* S,
    float* U, lapack_int const* ldu,
    float* VT, lapack_int const* ldvt,
    float* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgesvdx(...) LAPACK_sgesvdx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sgesvdx(...) LAPACK_sgesvdx_base(__VA_ARGS__)
#endif

#define LAPACK_zgesvdx_base LAPACK_GLOBAL(zgesvdx,ZGESVDX)
void LAPACK_zgesvdx_base(
    char const* jobu, char const* jobvt, char const* range,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double const* vl,
    double const* vu, lapack_int const* il, lapack_int const* iu, lapack_int* ns,
    double* S,
    lapack_complex_double* U, lapack_int const* ldu,
    lapack_complex_double* VT, lapack_int const* ldvt,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgesvdx(...) LAPACK_zgesvdx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zgesvdx(...) LAPACK_zgesvdx_base(__VA_ARGS__)
#endif

#define LAPACK_cgesvj_base LAPACK_GLOBAL(cgesvj,CGESVJ)
void LAPACK_cgesvj_base(
    char const* joba, char const* jobu, char const* jobv,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* SVA, lapack_int const* mv,
    lapack_complex_float* V, lapack_int const* ldv,
    lapack_complex_float* cwork, lapack_int const* lwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgesvj(...) LAPACK_cgesvj_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cgesvj(...) LAPACK_cgesvj_base(__VA_ARGS__)
#endif

#define LAPACK_dgesvj_base LAPACK_GLOBAL(dgesvj,DGESVJ)
void LAPACK_dgesvj_base(
    char const* joba, char const* jobu, char const* jobv,
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* SVA, lapack_int const* mv,
    double* V, lapack_int const* ldv,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgesvj(...) LAPACK_dgesvj_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dgesvj(...) LAPACK_dgesvj_base(__VA_ARGS__)
#endif

#define LAPACK_sgesvj_base LAPACK_GLOBAL(sgesvj,SGESVJ)
void LAPACK_sgesvj_base(
    char const* joba, char const* jobu, char const* jobv,
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* SVA, lapack_int const* mv,
    float* V, lapack_int const* ldv,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgesvj(...) LAPACK_sgesvj_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sgesvj(...) LAPACK_sgesvj_base(__VA_ARGS__)
#endif

#define LAPACK_zgesvj_base LAPACK_GLOBAL(zgesvj,ZGESVJ)
void LAPACK_zgesvj_base(
    char const* joba, char const* jobu, char const* jobv,
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* SVA, lapack_int const* mv,
    lapack_complex_double* V, lapack_int const* ldv,
    lapack_complex_double* cwork, lapack_int const* lwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgesvj(...) LAPACK_zgesvj_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zgesvj(...) LAPACK_zgesvj_base(__VA_ARGS__)
#endif

#define LAPACK_cgesvx_base LAPACK_GLOBAL(cgesvx,CGESVX)
void LAPACK_cgesvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* AF, lapack_int const* ldaf, lapack_int* ipiv, char* equed,
    float* R,
    float* C,
    lapack_complex_float* B,
    lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* rcond,
    float* ferr,
    float* berr,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgesvx(...) LAPACK_cgesvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cgesvx(...) LAPACK_cgesvx_base(__VA_ARGS__)
#endif

#define LAPACK_dgesvx_base LAPACK_GLOBAL(dgesvx,DGESVX)
void LAPACK_dgesvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    double* A, lapack_int const* lda,
    double* AF, lapack_int const* ldaf, lapack_int* ipiv, char* equed,
    double* R,
    double* C,
    double* B,
    lapack_int const* ldb,
    double* X, lapack_int const* ldx,
    double* rcond,
    double* ferr,
    double* berr,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgesvx(...) LAPACK_dgesvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dgesvx(...) LAPACK_dgesvx_base(__VA_ARGS__)
#endif

#define LAPACK_sgesvx_base LAPACK_GLOBAL(sgesvx,SGESVX)
void LAPACK_sgesvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    float* A, lapack_int const* lda,
    float* AF, lapack_int const* ldaf, lapack_int* ipiv, char* equed,
    float* R,
    float* C,
    float* B,
    lapack_int const* ldb,
    float* X, lapack_int const* ldx,
    float* rcond,
    float* ferr,
    float* berr,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgesvx(...) LAPACK_sgesvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sgesvx(...) LAPACK_sgesvx_base(__VA_ARGS__)
#endif

#define LAPACK_zgesvx_base LAPACK_GLOBAL(zgesvx,ZGESVX)
void LAPACK_zgesvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* AF, lapack_int const* ldaf, lapack_int* ipiv, char* equed,
    double* R,
    double* C,
    lapack_complex_double* B,
    lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* rcond,
    double* ferr,
    double* berr,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgesvx(...) LAPACK_zgesvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zgesvx(...) LAPACK_zgesvx_base(__VA_ARGS__)
#endif

#define LAPACK_cgesvxx_base LAPACK_GLOBAL(cgesvxx,CGESVXX)
void LAPACK_cgesvxx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* AF, lapack_int const* ldaf, lapack_int* ipiv, char* equed,
    float* R,
    float* C,
    lapack_complex_float* B,
    lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* rcond,
    float* rpvgrw,
    float* berr, lapack_int const* n_err_bnds,
    float* err_bnds_norm,
    float* err_bnds_comp, lapack_int const* nparams,
    float* params,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgesvxx(...) LAPACK_cgesvxx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cgesvxx(...) LAPACK_cgesvxx_base(__VA_ARGS__)
#endif

#define LAPACK_dgesvxx_base LAPACK_GLOBAL(dgesvxx,DGESVXX)
void LAPACK_dgesvxx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    double* A, lapack_int const* lda,
    double* AF, lapack_int const* ldaf, lapack_int* ipiv, char* equed,
    double* R,
    double* C,
    double* B,
    lapack_int const* ldb,
    double* X, lapack_int const* ldx,
    double* rcond,
    double* rpvgrw,
    double* berr, lapack_int const* n_err_bnds,
    double* err_bnds_norm,
    double* err_bnds_comp, lapack_int const* nparams,
    double* params,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgesvxx(...) LAPACK_dgesvxx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dgesvxx(...) LAPACK_dgesvxx_base(__VA_ARGS__)
#endif

#define LAPACK_sgesvxx_base LAPACK_GLOBAL(sgesvxx,SGESVXX)
void LAPACK_sgesvxx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    float* A, lapack_int const* lda,
    float* AF, lapack_int const* ldaf, lapack_int* ipiv, char* equed,
    float* R,
    float* C,
    float* B,
    lapack_int const* ldb,
    float* X, lapack_int const* ldx,
    float* rcond,
    float* rpvgrw,
    float* berr, lapack_int const* n_err_bnds,
    float* err_bnds_norm,
    float* err_bnds_comp, lapack_int const* nparams,
    float* params,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgesvxx(...) LAPACK_sgesvxx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sgesvxx(...) LAPACK_sgesvxx_base(__VA_ARGS__)
#endif

#define LAPACK_zgesvxx_base LAPACK_GLOBAL(zgesvxx,ZGESVXX)
void LAPACK_zgesvxx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* AF, lapack_int const* ldaf, lapack_int* ipiv, char* equed,
    double* R,
    double* C,
    lapack_complex_double* B,
    lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* rcond,
    double* rpvgrw,
    double* berr, lapack_int const* n_err_bnds,
    double* err_bnds_norm,
    double* err_bnds_comp, lapack_int const* nparams,
    double* params,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgesvxx(...) LAPACK_zgesvxx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zgesvxx(...) LAPACK_zgesvxx_base(__VA_ARGS__)
#endif

#define LAPACK_cgetf2 LAPACK_GLOBAL(cgetf2,CGETF2)
void LAPACK_cgetf2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_dgetf2 LAPACK_GLOBAL(dgetf2,DGETF2)
void LAPACK_dgetf2(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_sgetf2 LAPACK_GLOBAL(sgetf2,SGETF2)
void LAPACK_sgetf2(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_zgetf2 LAPACK_GLOBAL(zgetf2,ZGETF2)
void LAPACK_zgetf2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_cgetrf LAPACK_GLOBAL(cgetrf,CGETRF)
void LAPACK_cgetrf(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_dgetrf LAPACK_GLOBAL(dgetrf,DGETRF)
void LAPACK_dgetrf(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_sgetrf LAPACK_GLOBAL(sgetrf,SGETRF)
void LAPACK_sgetrf(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_zgetrf LAPACK_GLOBAL(zgetrf,ZGETRF)
void LAPACK_zgetrf(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_cgetrf2 LAPACK_GLOBAL(cgetrf2,CGETRF2)
void LAPACK_cgetrf2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_dgetrf2 LAPACK_GLOBAL(dgetrf2,DGETRF2)
void LAPACK_dgetrf2(
    lapack_int const* m, lapack_int const* n,
    double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_sgetrf2 LAPACK_GLOBAL(sgetrf2,SGETRF2)
void LAPACK_sgetrf2(
    lapack_int const* m, lapack_int const* n,
    float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_zgetrf2 LAPACK_GLOBAL(zgetrf2,ZGETRF2)
void LAPACK_zgetrf2(
    lapack_int const* m, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_cgetri LAPACK_GLOBAL(cgetri,CGETRI)
void LAPACK_cgetri(
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int const* ipiv,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgetri LAPACK_GLOBAL(dgetri,DGETRI)
void LAPACK_dgetri(
    lapack_int const* n,
    double* A, lapack_int const* lda, lapack_int const* ipiv,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgetri LAPACK_GLOBAL(sgetri,SGETRI)
void LAPACK_sgetri(
    lapack_int const* n,
    float* A, lapack_int const* lda, lapack_int const* ipiv,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgetri LAPACK_GLOBAL(zgetri,ZGETRI)
void LAPACK_zgetri(
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int const* ipiv,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cgetrs_base LAPACK_GLOBAL(cgetrs,CGETRS)
void LAPACK_cgetrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float const* A, lapack_int const* lda, lapack_int const* ipiv,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgetrs(...) LAPACK_cgetrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgetrs(...) LAPACK_cgetrs_base(__VA_ARGS__)
#endif

#define LAPACK_dgetrs_base LAPACK_GLOBAL(dgetrs,DGETRS)
void LAPACK_dgetrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    double const* A, lapack_int const* lda, lapack_int const* ipiv,
    double* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgetrs(...) LAPACK_dgetrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgetrs(...) LAPACK_dgetrs_base(__VA_ARGS__)
#endif

#define LAPACK_sgetrs_base LAPACK_GLOBAL(sgetrs,SGETRS)
void LAPACK_sgetrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    float const* A, lapack_int const* lda, lapack_int const* ipiv,
    float* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgetrs(...) LAPACK_sgetrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgetrs(...) LAPACK_sgetrs_base(__VA_ARGS__)
#endif

#define LAPACK_zgetrs_base LAPACK_GLOBAL(zgetrs,ZGETRS)
void LAPACK_zgetrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double const* A, lapack_int const* lda, lapack_int const* ipiv,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgetrs(...) LAPACK_zgetrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgetrs(...) LAPACK_zgetrs_base(__VA_ARGS__)
#endif

#define LAPACK_cgetsls_base LAPACK_GLOBAL(cgetsls,CGETSLS)
void LAPACK_cgetsls_base(
    char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgetsls(...) LAPACK_cgetsls_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgetsls(...) LAPACK_cgetsls_base(__VA_ARGS__)
#endif

#define LAPACK_dgetsls_base LAPACK_GLOBAL(dgetsls,DGETSLS)
void LAPACK_dgetsls_base(
    char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgetsls(...) LAPACK_dgetsls_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgetsls(...) LAPACK_dgetsls_base(__VA_ARGS__)
#endif

#define LAPACK_sgetsls_base LAPACK_GLOBAL(sgetsls,SGETSLS)
void LAPACK_sgetsls_base(
    char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgetsls(...) LAPACK_sgetsls_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgetsls(...) LAPACK_sgetsls_base(__VA_ARGS__)
#endif

#define LAPACK_zgetsls_base LAPACK_GLOBAL(zgetsls,ZGETSLS)
void LAPACK_zgetsls_base(
    char const* trans,
    lapack_int const* m, lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgetsls(...) LAPACK_zgetsls_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgetsls(...) LAPACK_zgetsls_base(__VA_ARGS__)
#endif

#define LAPACK_cgetsqrhrt LAPACK_GLOBAL(cgetsqrhrt,CGETSQRHRT)
void LAPACK_cgetsqrhrt(
    lapack_int const* m, lapack_int const* n,
    lapack_int const* mb1, lapack_int const* nb1, lapack_int const* nb2,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* T, lapack_int const* ldt,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgetsqrhrt LAPACK_GLOBAL(dgetsqrhrt,DGETSQRHRT)
void LAPACK_dgetsqrhrt(
    lapack_int const* m, lapack_int const* n,
    lapack_int const* mb1, lapack_int const* nb1, lapack_int const* nb2,
    double* A, lapack_int const* lda,
    double* T, lapack_int const* ldt,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgetsqrhrt LAPACK_GLOBAL(sgetsqrhrt,SGETSQRHRT)
void LAPACK_sgetsqrhrt(
    lapack_int const* m, lapack_int const* n,
    lapack_int const* mb1, lapack_int const* nb1, lapack_int const* nb2,
    float* A, lapack_int const* lda,
    float* T, lapack_int const* ldt,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgetsqrhrt LAPACK_GLOBAL(zgetsqrhrt,ZGETSQRHRT)
void LAPACK_zgetsqrhrt(
    lapack_int const* m, lapack_int const* n,
    lapack_int const* mb1, lapack_int const* nb1, lapack_int const* nb2,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* T, lapack_int const* ldt,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cggbak_base LAPACK_GLOBAL(cggbak,CGGBAK)
void LAPACK_cggbak_base(
    char const* job, char const* side,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    float const* lscale,
    float const* rscale, lapack_int const* m,
    lapack_complex_float* V, lapack_int const* ldv,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cggbak(...) LAPACK_cggbak_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cggbak(...) LAPACK_cggbak_base(__VA_ARGS__)
#endif

#define LAPACK_dggbak_base LAPACK_GLOBAL(dggbak,DGGBAK)
void LAPACK_dggbak_base(
    char const* job, char const* side,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    double const* lscale,
    double const* rscale, lapack_int const* m,
    double* V, lapack_int const* ldv,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dggbak(...) LAPACK_dggbak_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dggbak(...) LAPACK_dggbak_base(__VA_ARGS__)
#endif

#define LAPACK_sggbak_base LAPACK_GLOBAL(sggbak,SGGBAK)
void LAPACK_sggbak_base(
    char const* job, char const* side,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    float const* lscale,
    float const* rscale, lapack_int const* m,
    float* V, lapack_int const* ldv,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sggbak(...) LAPACK_sggbak_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sggbak(...) LAPACK_sggbak_base(__VA_ARGS__)
#endif

#define LAPACK_zggbak_base LAPACK_GLOBAL(zggbak,ZGGBAK)
void LAPACK_zggbak_base(
    char const* job, char const* side,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    double const* lscale,
    double const* rscale, lapack_int const* m,
    lapack_complex_double* V, lapack_int const* ldv,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zggbak(...) LAPACK_zggbak_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zggbak(...) LAPACK_zggbak_base(__VA_ARGS__)
#endif

#define LAPACK_cggbal_base LAPACK_GLOBAL(cggbal,CGGBAL)
void LAPACK_cggbal_base(
    char const* job,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb, lapack_int* ilo, lapack_int* ihi,
    float* lscale,
    float* rscale,
    float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cggbal(...) LAPACK_cggbal_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cggbal(...) LAPACK_cggbal_base(__VA_ARGS__)
#endif

#define LAPACK_dggbal_base LAPACK_GLOBAL(dggbal,DGGBAL)
void LAPACK_dggbal_base(
    char const* job,
    lapack_int const* n,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb, lapack_int* ilo, lapack_int* ihi,
    double* lscale,
    double* rscale,
    double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dggbal(...) LAPACK_dggbal_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dggbal(...) LAPACK_dggbal_base(__VA_ARGS__)
#endif

#define LAPACK_sggbal_base LAPACK_GLOBAL(sggbal,SGGBAL)
void LAPACK_sggbal_base(
    char const* job,
    lapack_int const* n,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb, lapack_int* ilo, lapack_int* ihi,
    float* lscale,
    float* rscale,
    float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sggbal(...) LAPACK_sggbal_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sggbal(...) LAPACK_sggbal_base(__VA_ARGS__)
#endif

#define LAPACK_zggbal_base LAPACK_GLOBAL(zggbal,ZGGBAL)
void LAPACK_zggbal_base(
    char const* job,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb, lapack_int* ilo, lapack_int* ihi,
    double* lscale,
    double* rscale,
    double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zggbal(...) LAPACK_zggbal_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zggbal(...) LAPACK_zggbal_base(__VA_ARGS__)
#endif

#define LAPACK_cgges_base LAPACK_GLOBAL(cgges,CGGES)
void LAPACK_cgges_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_C_SELECT2 selctg,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb, lapack_int* sdim,
    lapack_complex_float* alpha,
    lapack_complex_float* beta,
    lapack_complex_float* VSL, lapack_int const* ldvsl,
    lapack_complex_float* VSR, lapack_int const* ldvsr,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgges(...) LAPACK_cgges_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cgges(...) LAPACK_cgges_base(__VA_ARGS__)
#endif

#define LAPACK_dgges_base LAPACK_GLOBAL(dgges,DGGES)
void LAPACK_dgges_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_D_SELECT3 selctg,
    lapack_int const* n,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb, lapack_int* sdim,
    double* alphar,
    double* alphai,
    double* beta,
    double* VSL, lapack_int const* ldvsl,
    double* VSR, lapack_int const* ldvsr,
    double* work, lapack_int const* lwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgges(...) LAPACK_dgges_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dgges(...) LAPACK_dgges_base(__VA_ARGS__)
#endif

#define LAPACK_sgges_base LAPACK_GLOBAL(sgges,SGGES)
void LAPACK_sgges_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_S_SELECT3 selctg,
    lapack_int const* n,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb, lapack_int* sdim,
    float* alphar,
    float* alphai,
    float* beta,
    float* VSL, lapack_int const* ldvsl,
    float* VSR, lapack_int const* ldvsr,
    float* work, lapack_int const* lwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgges(...) LAPACK_sgges_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sgges(...) LAPACK_sgges_base(__VA_ARGS__)
#endif

#define LAPACK_zgges_base LAPACK_GLOBAL(zgges,ZGGES)
void LAPACK_zgges_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_Z_SELECT2 selctg,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb, lapack_int* sdim,
    lapack_complex_double* alpha,
    lapack_complex_double* beta,
    lapack_complex_double* VSL, lapack_int const* ldvsl,
    lapack_complex_double* VSR, lapack_int const* ldvsr,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgges(...) LAPACK_zgges_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zgges(...) LAPACK_zgges_base(__VA_ARGS__)
#endif

#define LAPACK_cgges3_base LAPACK_GLOBAL(cgges3,CGGES3)
void LAPACK_cgges3_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_C_SELECT2 selctg,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb, lapack_int* sdim,
    lapack_complex_float* alpha,
    lapack_complex_float* beta,
    lapack_complex_float* VSL, lapack_int const* ldvsl,
    lapack_complex_float* VSR, lapack_int const* ldvsr,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgges3(...) LAPACK_cgges3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cgges3(...) LAPACK_cgges3_base(__VA_ARGS__)
#endif

#define LAPACK_dgges3_base LAPACK_GLOBAL(dgges3,DGGES3)
void LAPACK_dgges3_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_D_SELECT3 selctg,
    lapack_int const* n,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb, lapack_int* sdim,
    double* alphar,
    double* alphai,
    double* beta,
    double* VSL, lapack_int const* ldvsl,
    double* VSR, lapack_int const* ldvsr,
    double* work, lapack_int const* lwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgges3(...) LAPACK_dgges3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dgges3(...) LAPACK_dgges3_base(__VA_ARGS__)
#endif

#define LAPACK_sgges3_base LAPACK_GLOBAL(sgges3,SGGES3)
void LAPACK_sgges3_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_S_SELECT3 selctg,
    lapack_int const* n,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb, lapack_int* sdim,
    float* alphar,
    float* alphai,
    float* beta,
    float* VSL, lapack_int const* ldvsl,
    float* VSR, lapack_int const* ldvsr,
    float* work, lapack_int const* lwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgges3(...) LAPACK_sgges3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sgges3(...) LAPACK_sgges3_base(__VA_ARGS__)
#endif

#define LAPACK_zgges3_base LAPACK_GLOBAL(zgges3,ZGGES3)
void LAPACK_zgges3_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_Z_SELECT2 selctg,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb, lapack_int* sdim,
    lapack_complex_double* alpha,
    lapack_complex_double* beta,
    lapack_complex_double* VSL, lapack_int const* ldvsl,
    lapack_complex_double* VSR, lapack_int const* ldvsr,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgges3(...) LAPACK_zgges3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zgges3(...) LAPACK_zgges3_base(__VA_ARGS__)
#endif

#define LAPACK_cggesx_base LAPACK_GLOBAL(cggesx,CGGESX)
void LAPACK_cggesx_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_C_SELECT2 selctg, char const* sense,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb, lapack_int* sdim,
    lapack_complex_float* alpha,
    lapack_complex_float* beta,
    lapack_complex_float* VSL, lapack_int const* ldvsl,
    lapack_complex_float* VSR, lapack_int const* ldvsr,
    float* rconde,
    float* rcondv,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* iwork, lapack_int const* liwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cggesx(...) LAPACK_cggesx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_cggesx(...) LAPACK_cggesx_base(__VA_ARGS__)
#endif

#define LAPACK_dggesx_base LAPACK_GLOBAL(dggesx,DGGESX)
void LAPACK_dggesx_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_D_SELECT3 selctg, char const* sense,
    lapack_int const* n,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb, lapack_int* sdim,
    double* alphar,
    double* alphai,
    double* beta,
    double* VSL, lapack_int const* ldvsl,
    double* VSR, lapack_int const* ldvsr,
    double* rconde,
    double* rcondv,
    double* work, lapack_int const* lwork,
    lapack_int* iwork, lapack_int const* liwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dggesx(...) LAPACK_dggesx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_dggesx(...) LAPACK_dggesx_base(__VA_ARGS__)
#endif

#define LAPACK_sggesx_base LAPACK_GLOBAL(sggesx,SGGESX)
void LAPACK_sggesx_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_S_SELECT3 selctg, char const* sense,
    lapack_int const* n,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb, lapack_int* sdim,
    float* alphar,
    float* alphai,
    float* beta,
    float* VSL, lapack_int const* ldvsl,
    float* VSR, lapack_int const* ldvsr,
    float* rconde,
    float* rcondv,
    float* work, lapack_int const* lwork,
    lapack_int* iwork, lapack_int const* liwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sggesx(...) LAPACK_sggesx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_sggesx(...) LAPACK_sggesx_base(__VA_ARGS__)
#endif

#define LAPACK_zggesx_base LAPACK_GLOBAL(zggesx,ZGGESX)
void LAPACK_zggesx_base(
    char const* jobvsl, char const* jobvsr, char const* sort, LAPACK_Z_SELECT2 selctg, char const* sense,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb, lapack_int* sdim,
    lapack_complex_double* alpha,
    lapack_complex_double* beta,
    lapack_complex_double* VSL, lapack_int const* ldvsl,
    lapack_complex_double* VSR, lapack_int const* ldvsr,
    double* rconde,
    double* rcondv,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* iwork, lapack_int const* liwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zggesx(...) LAPACK_zggesx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_zggesx(...) LAPACK_zggesx_base(__VA_ARGS__)
#endif

#define LAPACK_cggev_base LAPACK_GLOBAL(cggev,CGGEV)
void LAPACK_cggev_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* alpha,
    lapack_complex_float* beta,
    lapack_complex_float* VL, lapack_int const* ldvl,
    lapack_complex_float* VR, lapack_int const* ldvr,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cggev(...) LAPACK_cggev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cggev(...) LAPACK_cggev_base(__VA_ARGS__)
#endif

#define LAPACK_dggev_base LAPACK_GLOBAL(dggev,DGGEV)
void LAPACK_dggev_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* alphar,
    double* alphai,
    double* beta,
    double* VL, lapack_int const* ldvl,
    double* VR, lapack_int const* ldvr,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dggev(...) LAPACK_dggev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dggev(...) LAPACK_dggev_base(__VA_ARGS__)
#endif

#define LAPACK_sggev_base LAPACK_GLOBAL(sggev,SGGEV)
void LAPACK_sggev_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* alphar,
    float* alphai,
    float* beta,
    float* VL, lapack_int const* ldvl,
    float* VR, lapack_int const* ldvr,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sggev(...) LAPACK_sggev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sggev(...) LAPACK_sggev_base(__VA_ARGS__)
#endif

#define LAPACK_zggev_base LAPACK_GLOBAL(zggev,ZGGEV)
void LAPACK_zggev_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* alpha,
    lapack_complex_double* beta,
    lapack_complex_double* VL, lapack_int const* ldvl,
    lapack_complex_double* VR, lapack_int const* ldvr,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zggev(...) LAPACK_zggev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zggev(...) LAPACK_zggev_base(__VA_ARGS__)
#endif

#define LAPACK_cggev3_base LAPACK_GLOBAL(cggev3,CGGEV3)
void LAPACK_cggev3_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* alpha,
    lapack_complex_float* beta,
    lapack_complex_float* VL, lapack_int const* ldvl,
    lapack_complex_float* VR, lapack_int const* ldvr,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cggev3(...) LAPACK_cggev3_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cggev3(...) LAPACK_cggev3_base(__VA_ARGS__)
#endif

#define LAPACK_dggev3_base LAPACK_GLOBAL(dggev3,DGGEV3)
void LAPACK_dggev3_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* alphar,
    double* alphai,
    double* beta,
    double* VL, lapack_int const* ldvl,
    double* VR, lapack_int const* ldvr,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dggev3(...) LAPACK_dggev3_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dggev3(...) LAPACK_dggev3_base(__VA_ARGS__)
#endif

#define LAPACK_sggev3_base LAPACK_GLOBAL(sggev3,SGGEV3)
void LAPACK_sggev3_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* alphar,
    float* alphai,
    float* beta,
    float* VL, lapack_int const* ldvl,
    float* VR, lapack_int const* ldvr,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sggev3(...) LAPACK_sggev3_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sggev3(...) LAPACK_sggev3_base(__VA_ARGS__)
#endif

#define LAPACK_zggev3_base LAPACK_GLOBAL(zggev3,ZGGEV3)
void LAPACK_zggev3_base(
    char const* jobvl, char const* jobvr,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* alpha,
    lapack_complex_double* beta,
    lapack_complex_double* VL, lapack_int const* ldvl,
    lapack_complex_double* VR, lapack_int const* ldvr,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zggev3(...) LAPACK_zggev3_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zggev3(...) LAPACK_zggev3_base(__VA_ARGS__)
#endif

#define LAPACK_cggevx_base LAPACK_GLOBAL(cggevx,CGGEVX)
void LAPACK_cggevx_base(
    char const* balanc, char const* jobvl, char const* jobvr, char const* sense,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* alpha,
    lapack_complex_float* beta,
    lapack_complex_float* VL, lapack_int const* ldvl,
    lapack_complex_float* VR, lapack_int const* ldvr, lapack_int* ilo, lapack_int* ihi,
    float* lscale,
    float* rscale,
    float* abnrm,
    float* bbnrm,
    float* rconde,
    float* rcondv,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* iwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cggevx(...) LAPACK_cggevx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_cggevx(...) LAPACK_cggevx_base(__VA_ARGS__)
#endif

#define LAPACK_dggevx_base LAPACK_GLOBAL(dggevx,DGGEVX)
void LAPACK_dggevx_base(
    char const* balanc, char const* jobvl, char const* jobvr, char const* sense,
    lapack_int const* n,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* alphar,
    double* alphai,
    double* beta,
    double* VL, lapack_int const* ldvl,
    double* VR, lapack_int const* ldvr, lapack_int* ilo, lapack_int* ihi,
    double* lscale,
    double* rscale,
    double* abnrm,
    double* bbnrm,
    double* rconde,
    double* rcondv,
    double* work, lapack_int const* lwork,
    lapack_int* iwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dggevx(...) LAPACK_dggevx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_dggevx(...) LAPACK_dggevx_base(__VA_ARGS__)
#endif

#define LAPACK_sggevx_base LAPACK_GLOBAL(sggevx,SGGEVX)
void LAPACK_sggevx_base(
    char const* balanc, char const* jobvl, char const* jobvr, char const* sense,
    lapack_int const* n,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* alphar,
    float* alphai,
    float* beta,
    float* VL, lapack_int const* ldvl,
    float* VR, lapack_int const* ldvr, lapack_int* ilo, lapack_int* ihi,
    float* lscale,
    float* rscale,
    float* abnrm,
    float* bbnrm,
    float* rconde,
    float* rcondv,
    float* work, lapack_int const* lwork,
    lapack_int* iwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sggevx(...) LAPACK_sggevx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_sggevx(...) LAPACK_sggevx_base(__VA_ARGS__)
#endif

#define LAPACK_zggevx_base LAPACK_GLOBAL(zggevx,ZGGEVX)
void LAPACK_zggevx_base(
    char const* balanc, char const* jobvl, char const* jobvr, char const* sense,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* alpha,
    lapack_complex_double* beta,
    lapack_complex_double* VL, lapack_int const* ldvl,
    lapack_complex_double* VR, lapack_int const* ldvr, lapack_int* ilo, lapack_int* ihi,
    double* lscale,
    double* rscale,
    double* abnrm,
    double* bbnrm,
    double* rconde,
    double* rcondv,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* iwork, lapack_logical* BWORK,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zggevx(...) LAPACK_zggevx_base(__VA_ARGS__, 1, 1, 1, 1)
#else
    #define LAPACK_zggevx(...) LAPACK_zggevx_base(__VA_ARGS__)
#endif

#define LAPACK_cggglm LAPACK_GLOBAL(cggglm,CGGGLM)
void LAPACK_cggglm(
    lapack_int const* n, lapack_int const* m, lapack_int const* p,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* D,
    lapack_complex_float* X,
    lapack_complex_float* Y,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dggglm LAPACK_GLOBAL(dggglm,DGGGLM)
void LAPACK_dggglm(
    lapack_int const* n, lapack_int const* m, lapack_int const* p,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* D,
    double* X,
    double* Y,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sggglm LAPACK_GLOBAL(sggglm,SGGGLM)
void LAPACK_sggglm(
    lapack_int const* n, lapack_int const* m, lapack_int const* p,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* D,
    float* X,
    float* Y,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zggglm LAPACK_GLOBAL(zggglm,ZGGGLM)
void LAPACK_zggglm(
    lapack_int const* n, lapack_int const* m, lapack_int const* p,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* D,
    lapack_complex_double* X,
    lapack_complex_double* Y,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cgghd3_base LAPACK_GLOBAL(cgghd3,CGGHD3)
void LAPACK_cgghd3_base(
    char const* compq, char const* compz,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* Q, lapack_int const* ldq,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgghd3(...) LAPACK_cgghd3_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgghd3(...) LAPACK_cgghd3_base(__VA_ARGS__)
#endif

#define LAPACK_dgghd3_base LAPACK_GLOBAL(dgghd3,DGGHD3)
void LAPACK_dgghd3_base(
    char const* compq, char const* compz,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* Q, lapack_int const* ldq,
    double* Z, lapack_int const* ldz,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgghd3(...) LAPACK_dgghd3_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgghd3(...) LAPACK_dgghd3_base(__VA_ARGS__)
#endif

#define LAPACK_sgghd3_base LAPACK_GLOBAL(sgghd3,SGGHD3)
void LAPACK_sgghd3_base(
    char const* compq, char const* compz,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* Q, lapack_int const* ldq,
    float* Z, lapack_int const* ldz,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgghd3(...) LAPACK_sgghd3_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgghd3(...) LAPACK_sgghd3_base(__VA_ARGS__)
#endif

#define LAPACK_zgghd3_base LAPACK_GLOBAL(zgghd3,ZGGHD3)
void LAPACK_zgghd3_base(
    char const* compq, char const* compz,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* Q, lapack_int const* ldq,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgghd3(...) LAPACK_zgghd3_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgghd3(...) LAPACK_zgghd3_base(__VA_ARGS__)
#endif

#define LAPACK_cgghrd_base LAPACK_GLOBAL(cgghrd,CGGHRD)
void LAPACK_cgghrd_base(
    char const* compq, char const* compz,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* Q, lapack_int const* ldq,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgghrd(...) LAPACK_cgghrd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgghrd(...) LAPACK_cgghrd_base(__VA_ARGS__)
#endif

#define LAPACK_dgghrd_base LAPACK_GLOBAL(dgghrd,DGGHRD)
void LAPACK_dgghrd_base(
    char const* compq, char const* compz,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* Q, lapack_int const* ldq,
    double* Z, lapack_int const* ldz,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgghrd(...) LAPACK_dgghrd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgghrd(...) LAPACK_dgghrd_base(__VA_ARGS__)
#endif

#define LAPACK_sgghrd_base LAPACK_GLOBAL(sgghrd,SGGHRD)
void LAPACK_sgghrd_base(
    char const* compq, char const* compz,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* Q, lapack_int const* ldq,
    float* Z, lapack_int const* ldz,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgghrd(...) LAPACK_sgghrd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgghrd(...) LAPACK_sgghrd_base(__VA_ARGS__)
#endif

#define LAPACK_zgghrd_base LAPACK_GLOBAL(zgghrd,ZGGHRD)
void LAPACK_zgghrd_base(
    char const* compq, char const* compz,
    lapack_int const* n, lapack_int const* ilo, lapack_int const* ihi,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* Q, lapack_int const* ldq,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgghrd(...) LAPACK_zgghrd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgghrd(...) LAPACK_zgghrd_base(__VA_ARGS__)
#endif

#define LAPACK_cgglse LAPACK_GLOBAL(cgglse,CGGLSE)
void LAPACK_cgglse(
    lapack_int const* m, lapack_int const* n, lapack_int const* p,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* C,
    lapack_complex_float* D,
    lapack_complex_float* X,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dgglse LAPACK_GLOBAL(dgglse,DGGLSE)
void LAPACK_dgglse(
    lapack_int const* m, lapack_int const* n, lapack_int const* p,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* C,
    double* D,
    double* X,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sgglse LAPACK_GLOBAL(sgglse,SGGLSE)
void LAPACK_sgglse(
    lapack_int const* m, lapack_int const* n, lapack_int const* p,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* C,
    float* D,
    float* X,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zgglse LAPACK_GLOBAL(zgglse,ZGGLSE)
void LAPACK_zgglse(
    lapack_int const* m, lapack_int const* n, lapack_int const* p,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* C,
    lapack_complex_double* D,
    lapack_complex_double* X,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cggqrf LAPACK_GLOBAL(cggqrf,CGGQRF)
void LAPACK_cggqrf(
    lapack_int const* n, lapack_int const* m, lapack_int const* p,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* taua,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* taub,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dggqrf LAPACK_GLOBAL(dggqrf,DGGQRF)
void LAPACK_dggqrf(
    lapack_int const* n, lapack_int const* m, lapack_int const* p,
    double* A, lapack_int const* lda,
    double* taua,
    double* B, lapack_int const* ldb,
    double* taub,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sggqrf LAPACK_GLOBAL(sggqrf,SGGQRF)
void LAPACK_sggqrf(
    lapack_int const* n, lapack_int const* m, lapack_int const* p,
    float* A, lapack_int const* lda,
    float* taua,
    float* B, lapack_int const* ldb,
    float* taub,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zggqrf LAPACK_GLOBAL(zggqrf,ZGGQRF)
void LAPACK_zggqrf(
    lapack_int const* n, lapack_int const* m, lapack_int const* p,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* taua,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* taub,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cggrqf LAPACK_GLOBAL(cggrqf,CGGRQF)
void LAPACK_cggrqf(
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* taua,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* taub,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_dggrqf LAPACK_GLOBAL(dggrqf,DGGRQF)
void LAPACK_dggrqf(
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* taua,
    double* B, lapack_int const* ldb,
    double* taub,
    double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_sggrqf LAPACK_GLOBAL(sggrqf,SGGRQF)
void LAPACK_sggrqf(
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* taua,
    float* B, lapack_int const* ldb,
    float* taub,
    float* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_zggrqf LAPACK_GLOBAL(zggrqf,ZGGRQF)
void LAPACK_zggrqf(
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* taua,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* taub,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info );

#define LAPACK_cggsvd_base LAPACK_GLOBAL(cggsvd,CGGSVD)
lapack_int LAPACK_cggsvd_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* n, lapack_int const* p,
    lapack_int* k, lapack_int* l,
    lapack_complex_float* a, lapack_int const* lda,
    lapack_complex_float* b, lapack_int const* ldb,
    float* alpha, float* beta,
    lapack_complex_float* u, lapack_int const* ldu,
    lapack_complex_float* v, lapack_int const* ldv,
    lapack_complex_float* q, lapack_int const* ldq,
    lapack_complex_float* work, float* rwork,
    lapack_int* iwork, lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cggsvd(...) LAPACK_cggsvd_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cggsvd(...) LAPACK_cggsvd_base(__VA_ARGS__)
#endif

#define LAPACK_sggsvd_base LAPACK_GLOBAL(sggsvd,SGGSVD)
lapack_int LAPACK_sggsvd_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* n, lapack_int const* p,
    lapack_int* k, lapack_int* l,
    float* a, lapack_int const* lda,
    float* b, lapack_int const* ldb,
    float* alpha, float* beta,
    float* u, lapack_int const* ldu,
    float* v, lapack_int const* ldv,
    float* q, lapack_int const* ldq,
    float* work, lapack_int* iwork, lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sggsvd(...) LAPACK_sggsvd_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sggsvd(...) LAPACK_sggsvd_base(__VA_ARGS__)
#endif

#define LAPACK_dggsvd_base LAPACK_GLOBAL(dggsvd,DGGSVD)
lapack_int LAPACK_dggsvd_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* n, lapack_int const* p,
    lapack_int* k, lapack_int* l,
    double* a, lapack_int const* lda,
    double* b, lapack_int const* ldb,
    double* alpha, double* beta,
    double* u, lapack_int const* ldu,
    double* v, lapack_int const* ldv,
    double* q, lapack_int const* ldq,
    double* work, lapack_int* iwork, lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dggsvd(...) LAPACK_dggsvd_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dggsvd(...) LAPACK_dggsvd_base(__VA_ARGS__)
#endif

#define LAPACK_zggsvd_base LAPACK_GLOBAL(zggsvd,ZGGSVD)
lapack_int LAPACK_zggsvd_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* n, lapack_int const* p,
    lapack_int* k, lapack_int* l,
    lapack_complex_double* a, lapack_int const* lda,
    lapack_complex_double* b, lapack_int const* ldb,
    double* alpha, double* beta,
    lapack_complex_double* u, lapack_int const* ldu,
    lapack_complex_double* v, lapack_int const* ldv,
    lapack_complex_double* q, lapack_int const* ldq,
    lapack_complex_double* work, double* rwork,
    lapack_int* iwork, lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zggsvd(...) LAPACK_zggsvd_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zggsvd(...) LAPACK_zggsvd_base(__VA_ARGS__)
#endif

#define LAPACK_cggsvd3_base LAPACK_GLOBAL(cggsvd3,CGGSVD3)
void LAPACK_cggsvd3_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* n, lapack_int const* p, lapack_int* k, lapack_int* l,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    float* alpha,
    float* beta,
    lapack_complex_float* U, lapack_int const* ldu,
    lapack_complex_float* V, lapack_int const* ldv,
    lapack_complex_float* Q, lapack_int const* ldq,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cggsvd3(...) LAPACK_cggsvd3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cggsvd3(...) LAPACK_cggsvd3_base(__VA_ARGS__)
#endif

#define LAPACK_dggsvd3_base LAPACK_GLOBAL(dggsvd3,DGGSVD3)
void LAPACK_dggsvd3_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* n, lapack_int const* p, lapack_int* k, lapack_int* l,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double* alpha,
    double* beta,
    double* U, lapack_int const* ldu,
    double* V, lapack_int const* ldv,
    double* Q, lapack_int const* ldq,
    double* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dggsvd3(...) LAPACK_dggsvd3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dggsvd3(...) LAPACK_dggsvd3_base(__VA_ARGS__)
#endif

#define LAPACK_sggsvd3_base LAPACK_GLOBAL(sggsvd3,SGGSVD3)
void LAPACK_sggsvd3_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* n, lapack_int const* p, lapack_int* k, lapack_int* l,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float* alpha,
    float* beta,
    float* U, lapack_int const* ldu,
    float* V, lapack_int const* ldv,
    float* Q, lapack_int const* ldq,
    float* work, lapack_int const* lwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sggsvd3(...) LAPACK_sggsvd3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sggsvd3(...) LAPACK_sggsvd3_base(__VA_ARGS__)
#endif

#define LAPACK_zggsvd3_base LAPACK_GLOBAL(zggsvd3,ZGGSVD3)
void LAPACK_zggsvd3_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* n, lapack_int const* p, lapack_int* k, lapack_int* l,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    double* alpha,
    double* beta,
    lapack_complex_double* U, lapack_int const* ldu,
    lapack_complex_double* V, lapack_int const* ldv,
    lapack_complex_double* Q, lapack_int const* ldq,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zggsvd3(...) LAPACK_zggsvd3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zggsvd3(...) LAPACK_zggsvd3_base(__VA_ARGS__)
#endif

#define LAPACK_sggsvp_base LAPACK_GLOBAL(sggsvp,SGGSVP)
lapack_int LAPACK_sggsvp_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    float* a, lapack_int const* lda,
    float* b, lapack_int const* ldb,
    float* tola, float* tolb,
    lapack_int* k, lapack_int* l,
    float* u, lapack_int const* ldu,
    float* v, lapack_int const* ldv,
    float* q, lapack_int const* ldq,
    lapack_int* iwork, float* tau,
    float* work, lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sggsvp(...) LAPACK_sggsvp_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sggsvp(...) LAPACK_sggsvp_base(__VA_ARGS__)
#endif

#define LAPACK_dggsvp_base LAPACK_GLOBAL(dggsvp,DGGSVP)
lapack_int LAPACK_dggsvp_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    double* a, lapack_int const* lda,
    double* b, lapack_int const* ldb,
    double* tola, double* tolb,
    lapack_int* k, lapack_int* l,
    double* u, lapack_int const* ldu,
    double* v, lapack_int const* ldv,
    double* q, lapack_int const* ldq,
    lapack_int* iwork, double* tau,
    double* work, lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dggsvp(...) LAPACK_dggsvp_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dggsvp(...) LAPACK_dggsvp_base(__VA_ARGS__)
#endif

#define LAPACK_cggsvp_base LAPACK_GLOBAL(cggsvp,CGGSVP)
lapack_int LAPACK_cggsvp_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    lapack_complex_float* a, lapack_int const* lda,
    lapack_complex_float* b, lapack_int const* ldb,
    float* tola, float* tolb, lapack_int* k, lapack_int* l,
    lapack_complex_float* u, lapack_int const* ldu,
    lapack_complex_float* v, lapack_int const* ldv,
    lapack_complex_float* q, lapack_int const* ldq,
    lapack_int* iwork, float* rwork, lapack_complex_float* tau,
    lapack_complex_float* work, lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cggsvp(...) LAPACK_cggsvp_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cggsvp(...) LAPACK_cggsvp_base(__VA_ARGS__)
#endif

#define LAPACK_zggsvp_base LAPACK_GLOBAL(zggsvp,ZGGSVP)
lapack_int LAPACK_zggsvp_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    lapack_complex_double* a, lapack_int const* lda,
    lapack_complex_double* b, lapack_int const* ldb,
    double* tola, double* tolb, lapack_int* k, lapack_int* l,
    lapack_complex_double* u, lapack_int const* ldu,
    lapack_complex_double* v, lapack_int const* ldv,
    lapack_complex_double* q, lapack_int const* ldq,
    lapack_int* iwork, double* rwork, lapack_complex_double* tau,
    lapack_complex_double* work, lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zggsvp(...) LAPACK_zggsvp_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zggsvp(...) LAPACK_zggsvp_base(__VA_ARGS__)
#endif

#define LAPACK_cggsvp3_base LAPACK_GLOBAL(cggsvp3,CGGSVP3)
void LAPACK_cggsvp3_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    float const* tola,
    float const* tolb, lapack_int* k, lapack_int* l,
    lapack_complex_float* U, lapack_int const* ldu,
    lapack_complex_float* V, lapack_int const* ldv,
    lapack_complex_float* Q, lapack_int const* ldq,
    lapack_int* iwork,
    float* rwork,
    lapack_complex_float* tau,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cggsvp3(...) LAPACK_cggsvp3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cggsvp3(...) LAPACK_cggsvp3_base(__VA_ARGS__)
#endif

#define LAPACK_dggsvp3_base LAPACK_GLOBAL(dggsvp3,DGGSVP3)
void LAPACK_dggsvp3_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    double* A, lapack_int const* lda,
    double* B, lapack_int const* ldb,
    double const* tola,
    double const* tolb, lapack_int* k, lapack_int* l,
    double* U, lapack_int const* ldu,
    double* V, lapack_int const* ldv,
    double* Q, lapack_int const* ldq,
    lapack_int* iwork,
    double* tau,
    double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dggsvp3(...) LAPACK_dggsvp3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_dggsvp3(...) LAPACK_dggsvp3_base(__VA_ARGS__)
#endif

#define LAPACK_sggsvp3_base LAPACK_GLOBAL(sggsvp3,SGGSVP3)
void LAPACK_sggsvp3_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    float* A, lapack_int const* lda,
    float* B, lapack_int const* ldb,
    float const* tola,
    float const* tolb, lapack_int* k, lapack_int* l,
    float* U, lapack_int const* ldu,
    float* V, lapack_int const* ldv,
    float* Q, lapack_int const* ldq,
    lapack_int* iwork,
    float* tau,
    float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sggsvp3(...) LAPACK_sggsvp3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_sggsvp3(...) LAPACK_sggsvp3_base(__VA_ARGS__)
#endif

#define LAPACK_zggsvp3_base LAPACK_GLOBAL(zggsvp3,ZGGSVP3)
void LAPACK_zggsvp3_base(
    char const* jobu, char const* jobv, char const* jobq,
    lapack_int const* m, lapack_int const* p, lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    double const* tola,
    double const* tolb, lapack_int* k, lapack_int* l,
    lapack_complex_double* U, lapack_int const* ldu,
    lapack_complex_double* V, lapack_int const* ldv,
    lapack_complex_double* Q, lapack_int const* ldq,
    lapack_int* iwork,
    double* rwork,
    lapack_complex_double* tau,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zggsvp3(...) LAPACK_zggsvp3_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zggsvp3(...) LAPACK_zggsvp3_base(__VA_ARGS__)
#endif

#define LAPACK_cgtcon_base LAPACK_GLOBAL(cgtcon,CGTCON)
void LAPACK_cgtcon_base(
    char const* norm,
    lapack_int const* n,
    lapack_complex_float const* DL,
    lapack_complex_float const* D,
    lapack_complex_float const* DU,
    lapack_complex_float const* DU2, lapack_int const* ipiv,
    float const* anorm,
    float* rcond,
    lapack_complex_float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgtcon(...) LAPACK_cgtcon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgtcon(...) LAPACK_cgtcon_base(__VA_ARGS__)
#endif

#define LAPACK_dgtcon_base LAPACK_GLOBAL(dgtcon,DGTCON)
void LAPACK_dgtcon_base(
    char const* norm,
    lapack_int const* n,
    double const* DL,
    double const* D,
    double const* DU,
    double const* DU2, lapack_int const* ipiv,
    double const* anorm,
    double* rcond,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgtcon(...) LAPACK_dgtcon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgtcon(...) LAPACK_dgtcon_base(__VA_ARGS__)
#endif

#define LAPACK_sgtcon_base LAPACK_GLOBAL(sgtcon,SGTCON)
void LAPACK_sgtcon_base(
    char const* norm,
    lapack_int const* n,
    float const* DL,
    float const* D,
    float const* DU,
    float const* DU2, lapack_int const* ipiv,
    float const* anorm,
    float* rcond,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgtcon(...) LAPACK_sgtcon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgtcon(...) LAPACK_sgtcon_base(__VA_ARGS__)
#endif

#define LAPACK_zgtcon_base LAPACK_GLOBAL(zgtcon,ZGTCON)
void LAPACK_zgtcon_base(
    char const* norm,
    lapack_int const* n,
    lapack_complex_double const* DL,
    lapack_complex_double const* D,
    lapack_complex_double const* DU,
    lapack_complex_double const* DU2, lapack_int const* ipiv,
    double const* anorm,
    double* rcond,
    lapack_complex_double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgtcon(...) LAPACK_zgtcon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgtcon(...) LAPACK_zgtcon_base(__VA_ARGS__)
#endif

#define LAPACK_cgtrfs_base LAPACK_GLOBAL(cgtrfs,CGTRFS)
void LAPACK_cgtrfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float const* DL,
    lapack_complex_float const* D,
    lapack_complex_float const* DU,
    lapack_complex_float const* DLF,
    lapack_complex_float const* DF,
    lapack_complex_float const* DUF,
    lapack_complex_float const* DU2, lapack_int const* ipiv,
    lapack_complex_float const* B, lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* ferr,
    float* berr,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgtrfs(...) LAPACK_cgtrfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgtrfs(...) LAPACK_cgtrfs_base(__VA_ARGS__)
#endif

#define LAPACK_dgtrfs_base LAPACK_GLOBAL(dgtrfs,DGTRFS)
void LAPACK_dgtrfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    double const* DL,
    double const* D,
    double const* DU,
    double const* DLF,
    double const* DF,
    double const* DUF,
    double const* DU2, lapack_int const* ipiv,
    double const* B, lapack_int const* ldb,
    double* X, lapack_int const* ldx,
    double* ferr,
    double* berr,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgtrfs(...) LAPACK_dgtrfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgtrfs(...) LAPACK_dgtrfs_base(__VA_ARGS__)
#endif

#define LAPACK_sgtrfs_base LAPACK_GLOBAL(sgtrfs,SGTRFS)
void LAPACK_sgtrfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    float const* DL,
    float const* D,
    float const* DU,
    float const* DLF,
    float const* DF,
    float const* DUF,
    float const* DU2, lapack_int const* ipiv,
    float const* B, lapack_int const* ldb,
    float* X, lapack_int const* ldx,
    float* ferr,
    float* berr,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgtrfs(...) LAPACK_sgtrfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgtrfs(...) LAPACK_sgtrfs_base(__VA_ARGS__)
#endif

#define LAPACK_zgtrfs_base LAPACK_GLOBAL(zgtrfs,ZGTRFS)
void LAPACK_zgtrfs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double const* DL,
    lapack_complex_double const* D,
    lapack_complex_double const* DU,
    lapack_complex_double const* DLF,
    lapack_complex_double const* DF,
    lapack_complex_double const* DUF,
    lapack_complex_double const* DU2, lapack_int const* ipiv,
    lapack_complex_double const* B, lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* ferr,
    double* berr,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgtrfs(...) LAPACK_zgtrfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgtrfs(...) LAPACK_zgtrfs_base(__VA_ARGS__)
#endif

#define LAPACK_cgtsv LAPACK_GLOBAL(cgtsv,CGTSV)
void LAPACK_cgtsv(
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* DL,
    lapack_complex_float* D,
    lapack_complex_float* DU,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_dgtsv LAPACK_GLOBAL(dgtsv,DGTSV)
void LAPACK_dgtsv(
    lapack_int const* n, lapack_int const* nrhs,
    double* DL,
    double* D,
    double* DU,
    double* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_sgtsv LAPACK_GLOBAL(sgtsv,SGTSV)
void LAPACK_sgtsv(
    lapack_int const* n, lapack_int const* nrhs,
    float* DL,
    float* D,
    float* DU,
    float* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_zgtsv LAPACK_GLOBAL(zgtsv,ZGTSV)
void LAPACK_zgtsv(
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* DL,
    lapack_complex_double* D,
    lapack_complex_double* DU,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_int* info );

#define LAPACK_cgtsvx_base LAPACK_GLOBAL(cgtsvx,CGTSVX)
void LAPACK_cgtsvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float const* DL,
    lapack_complex_float const* D,
    lapack_complex_float const* DU,
    lapack_complex_float* DLF,
    lapack_complex_float* DF,
    lapack_complex_float* DUF,
    lapack_complex_float* DU2, lapack_int* ipiv,
    lapack_complex_float const* B, lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* rcond,
    float* ferr,
    float* berr,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgtsvx(...) LAPACK_cgtsvx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cgtsvx(...) LAPACK_cgtsvx_base(__VA_ARGS__)
#endif

#define LAPACK_dgtsvx_base LAPACK_GLOBAL(dgtsvx,DGTSVX)
void LAPACK_dgtsvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    double const* DL,
    double const* D,
    double const* DU,
    double* DLF,
    double* DF,
    double* DUF,
    double* DU2, lapack_int* ipiv,
    double const* B, lapack_int const* ldb,
    double* X, lapack_int const* ldx,
    double* rcond,
    double* ferr,
    double* berr,
    double* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgtsvx(...) LAPACK_dgtsvx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_dgtsvx(...) LAPACK_dgtsvx_base(__VA_ARGS__)
#endif

#define LAPACK_sgtsvx_base LAPACK_GLOBAL(sgtsvx,SGTSVX)
void LAPACK_sgtsvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    float const* DL,
    float const* D,
    float const* DU,
    float* DLF,
    float* DF,
    float* DUF,
    float* DU2, lapack_int* ipiv,
    float const* B, lapack_int const* ldb,
    float* X, lapack_int const* ldx,
    float* rcond,
    float* ferr,
    float* berr,
    float* work,
    lapack_int* iwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgtsvx(...) LAPACK_sgtsvx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_sgtsvx(...) LAPACK_sgtsvx_base(__VA_ARGS__)
#endif

#define LAPACK_zgtsvx_base LAPACK_GLOBAL(zgtsvx,ZGTSVX)
void LAPACK_zgtsvx_base(
    char const* fact, char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double const* DL,
    lapack_complex_double const* D,
    lapack_complex_double const* DU,
    lapack_complex_double* DLF,
    lapack_complex_double* DF,
    lapack_complex_double* DUF,
    lapack_complex_double* DU2, lapack_int* ipiv,
    lapack_complex_double const* B, lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* rcond,
    double* ferr,
    double* berr,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgtsvx(...) LAPACK_zgtsvx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zgtsvx(...) LAPACK_zgtsvx_base(__VA_ARGS__)
#endif

#define LAPACK_cgttrf LAPACK_GLOBAL(cgttrf,CGTTRF)
void LAPACK_cgttrf(
    lapack_int const* n,
    lapack_complex_float* DL,
    lapack_complex_float* D,
    lapack_complex_float* DU,
    lapack_complex_float* DU2, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_dgttrf LAPACK_GLOBAL(dgttrf,DGTTRF)
void LAPACK_dgttrf(
    lapack_int const* n,
    double* DL,
    double* D,
    double* DU,
    double* DU2, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_sgttrf LAPACK_GLOBAL(sgttrf,SGTTRF)
void LAPACK_sgttrf(
    lapack_int const* n,
    float* DL,
    float* D,
    float* DU,
    float* DU2, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_zgttrf LAPACK_GLOBAL(zgttrf,ZGTTRF)
void LAPACK_zgttrf(
    lapack_int const* n,
    lapack_complex_double* DL,
    lapack_complex_double* D,
    lapack_complex_double* DU,
    lapack_complex_double* DU2, lapack_int* ipiv,
    lapack_int* info );

#define LAPACK_cgttrs_base LAPACK_GLOBAL(cgttrs,CGTTRS)
void LAPACK_cgttrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float const* DL,
    lapack_complex_float const* D,
    lapack_complex_float const* DU,
    lapack_complex_float const* DU2, lapack_int const* ipiv,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cgttrs(...) LAPACK_cgttrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cgttrs(...) LAPACK_cgttrs_base(__VA_ARGS__)
#endif

#define LAPACK_dgttrs_base LAPACK_GLOBAL(dgttrs,DGTTRS)
void LAPACK_dgttrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    double const* DL,
    double const* D,
    double const* DU,
    double const* DU2, lapack_int const* ipiv,
    double* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_dgttrs(...) LAPACK_dgttrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_dgttrs(...) LAPACK_dgttrs_base(__VA_ARGS__)
#endif

#define LAPACK_sgttrs_base LAPACK_GLOBAL(sgttrs,SGTTRS)
void LAPACK_sgttrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    float const* DL,
    float const* D,
    float const* DU,
    float const* DU2, lapack_int const* ipiv,
    float* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_sgttrs(...) LAPACK_sgttrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_sgttrs(...) LAPACK_sgttrs_base(__VA_ARGS__)
#endif

#define LAPACK_zgttrs_base LAPACK_GLOBAL(zgttrs,ZGTTRS)
void LAPACK_zgttrs_base(
    char const* trans,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double const* DL,
    lapack_complex_double const* D,
    lapack_complex_double const* DU,
    lapack_complex_double const* DU2, lapack_int const* ipiv,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zgttrs(...) LAPACK_zgttrs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zgttrs(...) LAPACK_zgttrs_base(__VA_ARGS__)
#endif

#define LAPACK_chbev_base LAPACK_GLOBAL(chbev,CHBEV)
void LAPACK_chbev_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_float* AB, lapack_int const* ldab,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chbev(...) LAPACK_chbev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chbev(...) LAPACK_chbev_base(__VA_ARGS__)
#endif

#define LAPACK_zhbev_base LAPACK_GLOBAL(zhbev,ZHBEV)
void LAPACK_zhbev_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_double* AB, lapack_int const* ldab,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhbev(...) LAPACK_zhbev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhbev(...) LAPACK_zhbev_base(__VA_ARGS__)
#endif

#define LAPACK_chbev_2stage_base LAPACK_GLOBAL(chbev_2stage,CHBEV_2STAGE)
void LAPACK_chbev_2stage_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_float* AB, lapack_int const* ldab,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chbev_2stage(...) LAPACK_chbev_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chbev_2stage(...) LAPACK_chbev_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_zhbev_2stage_base LAPACK_GLOBAL(zhbev_2stage,ZHBEV_2STAGE)
void LAPACK_zhbev_2stage_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_double* AB, lapack_int const* ldab,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhbev_2stage(...) LAPACK_zhbev_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhbev_2stage(...) LAPACK_zhbev_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_chbevd_base LAPACK_GLOBAL(chbevd,CHBEVD)
void LAPACK_chbevd_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_float* AB, lapack_int const* ldab,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chbevd(...) LAPACK_chbevd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chbevd(...) LAPACK_chbevd_base(__VA_ARGS__)
#endif

#define LAPACK_zhbevd_base LAPACK_GLOBAL(zhbevd,ZHBEVD)
void LAPACK_zhbevd_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_double* AB, lapack_int const* ldab,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhbevd(...) LAPACK_zhbevd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhbevd(...) LAPACK_zhbevd_base(__VA_ARGS__)
#endif

#define LAPACK_chbevd_2stage_base LAPACK_GLOBAL(chbevd_2stage,CHBEVD_2STAGE)
void LAPACK_chbevd_2stage_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_float* AB, lapack_int const* ldab,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chbevd_2stage(...) LAPACK_chbevd_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chbevd_2stage(...) LAPACK_chbevd_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_zhbevd_2stage_base LAPACK_GLOBAL(zhbevd_2stage,ZHBEVD_2STAGE)
void LAPACK_zhbevd_2stage_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_double* AB, lapack_int const* ldab,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhbevd_2stage(...) LAPACK_zhbevd_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhbevd_2stage(...) LAPACK_zhbevd_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_chbevx_base LAPACK_GLOBAL(chbevx,CHBEVX)
void LAPACK_chbevx_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_float* AB, lapack_int const* ldab,
    lapack_complex_float* Q, lapack_int const* ldq,
    float const* vl,
    float const* vu, lapack_int const* il, lapack_int const* iu,
    float const* abstol, lapack_int* m,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chbevx(...) LAPACK_chbevx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_chbevx(...) LAPACK_chbevx_base(__VA_ARGS__)
#endif

#define LAPACK_zhbevx_base LAPACK_GLOBAL(zhbevx,ZHBEVX)
void LAPACK_zhbevx_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_double* AB, lapack_int const* ldab,
    lapack_complex_double* Q, lapack_int const* ldq,
    double const* vl,
    double const* vu, lapack_int const* il, lapack_int const* iu,
    double const* abstol, lapack_int* m,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhbevx(...) LAPACK_zhbevx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zhbevx(...) LAPACK_zhbevx_base(__VA_ARGS__)
#endif

#define LAPACK_chbevx_2stage_base LAPACK_GLOBAL(chbevx_2stage,CHBEVX_2STAGE)
void LAPACK_chbevx_2stage_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_float* AB, lapack_int const* ldab,
    lapack_complex_float* Q, lapack_int const* ldq,
    float const* vl,
    float const* vu, lapack_int const* il, lapack_int const* iu,
    float const* abstol, lapack_int* m,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chbevx_2stage(...) LAPACK_chbevx_2stage_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_chbevx_2stage(...) LAPACK_chbevx_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_zhbevx_2stage_base LAPACK_GLOBAL(zhbevx_2stage,ZHBEVX_2STAGE)
void LAPACK_zhbevx_2stage_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_double* AB, lapack_int const* ldab,
    lapack_complex_double* Q, lapack_int const* ldq,
    double const* vl,
    double const* vu, lapack_int const* il, lapack_int const* iu,
    double const* abstol, lapack_int* m,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhbevx_2stage(...) LAPACK_zhbevx_2stage_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zhbevx_2stage(...) LAPACK_zhbevx_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_chbgst_base LAPACK_GLOBAL(chbgst,CHBGST)
void LAPACK_chbgst_base(
    char const* vect, char const* uplo,
    lapack_int const* n, lapack_int const* ka, lapack_int const* kb,
    lapack_complex_float* AB, lapack_int const* ldab,
    lapack_complex_float const* BB, lapack_int const* ldbb,
    lapack_complex_float* X, lapack_int const* ldx,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chbgst(...) LAPACK_chbgst_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chbgst(...) LAPACK_chbgst_base(__VA_ARGS__)
#endif

#define LAPACK_zhbgst_base LAPACK_GLOBAL(zhbgst,ZHBGST)
void LAPACK_zhbgst_base(
    char const* vect, char const* uplo,
    lapack_int const* n, lapack_int const* ka, lapack_int const* kb,
    lapack_complex_double* AB, lapack_int const* ldab,
    lapack_complex_double const* BB, lapack_int const* ldbb,
    lapack_complex_double* X, lapack_int const* ldx,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhbgst(...) LAPACK_zhbgst_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhbgst(...) LAPACK_zhbgst_base(__VA_ARGS__)
#endif

#define LAPACK_chbgv_base LAPACK_GLOBAL(chbgv,CHBGV)
void LAPACK_chbgv_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* ka, lapack_int const* kb,
    lapack_complex_float* AB, lapack_int const* ldab,
    lapack_complex_float* BB, lapack_int const* ldbb,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chbgv(...) LAPACK_chbgv_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chbgv(...) LAPACK_chbgv_base(__VA_ARGS__)
#endif

#define LAPACK_zhbgv_base LAPACK_GLOBAL(zhbgv,ZHBGV)
void LAPACK_zhbgv_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* ka, lapack_int const* kb,
    lapack_complex_double* AB, lapack_int const* ldab,
    lapack_complex_double* BB, lapack_int const* ldbb,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhbgv(...) LAPACK_zhbgv_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhbgv(...) LAPACK_zhbgv_base(__VA_ARGS__)
#endif

#define LAPACK_chbgvd_base LAPACK_GLOBAL(chbgvd,CHBGVD)
void LAPACK_chbgvd_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* ka, lapack_int const* kb,
    lapack_complex_float* AB, lapack_int const* ldab,
    lapack_complex_float* BB, lapack_int const* ldbb,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chbgvd(...) LAPACK_chbgvd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chbgvd(...) LAPACK_chbgvd_base(__VA_ARGS__)
#endif

#define LAPACK_zhbgvd_base LAPACK_GLOBAL(zhbgvd,ZHBGVD)
void LAPACK_zhbgvd_base(
    char const* jobz, char const* uplo,
    lapack_int const* n, lapack_int const* ka, lapack_int const* kb,
    lapack_complex_double* AB, lapack_int const* ldab,
    lapack_complex_double* BB, lapack_int const* ldbb,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhbgvd(...) LAPACK_zhbgvd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhbgvd(...) LAPACK_zhbgvd_base(__VA_ARGS__)
#endif

#define LAPACK_chbgvx_base LAPACK_GLOBAL(chbgvx,CHBGVX)
void LAPACK_chbgvx_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n, lapack_int const* ka, lapack_int const* kb,
    lapack_complex_float* AB, lapack_int const* ldab,
    lapack_complex_float* BB, lapack_int const* ldbb,
    lapack_complex_float* Q, lapack_int const* ldq,
    float const* vl,
    float const* vu, lapack_int const* il, lapack_int const* iu,
    float const* abstol, lapack_int* m,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chbgvx(...) LAPACK_chbgvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_chbgvx(...) LAPACK_chbgvx_base(__VA_ARGS__)
#endif

#define LAPACK_zhbgvx_base LAPACK_GLOBAL(zhbgvx,ZHBGVX)
void LAPACK_zhbgvx_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n, lapack_int const* ka, lapack_int const* kb,
    lapack_complex_double* AB, lapack_int const* ldab,
    lapack_complex_double* BB, lapack_int const* ldbb,
    lapack_complex_double* Q, lapack_int const* ldq,
    double const* vl,
    double const* vu, lapack_int const* il, lapack_int const* iu,
    double const* abstol, lapack_int* m,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhbgvx(...) LAPACK_zhbgvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zhbgvx(...) LAPACK_zhbgvx_base(__VA_ARGS__)
#endif

#define LAPACK_chbtrd_base LAPACK_GLOBAL(chbtrd,CHBTRD)
void LAPACK_chbtrd_base(
    char const* vect, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_float* AB, lapack_int const* ldab,
    float* D,
    float* E,
    lapack_complex_float* Q, lapack_int const* ldq,
    lapack_complex_float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chbtrd(...) LAPACK_chbtrd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chbtrd(...) LAPACK_chbtrd_base(__VA_ARGS__)
#endif

#define LAPACK_zhbtrd_base LAPACK_GLOBAL(zhbtrd,ZHBTRD)
void LAPACK_zhbtrd_base(
    char const* vect, char const* uplo,
    lapack_int const* n, lapack_int const* kd,
    lapack_complex_double* AB, lapack_int const* ldab,
    double* D,
    double* E,
    lapack_complex_double* Q, lapack_int const* ldq,
    lapack_complex_double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhbtrd(...) LAPACK_zhbtrd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhbtrd(...) LAPACK_zhbtrd_base(__VA_ARGS__)
#endif

#define LAPACK_checon_base LAPACK_GLOBAL(checon,CHECON)
void LAPACK_checon_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float const* A, lapack_int const* lda, lapack_int const* ipiv,
    float const* anorm,
    float* rcond,
    lapack_complex_float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_checon(...) LAPACK_checon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_checon(...) LAPACK_checon_base(__VA_ARGS__)
#endif

#define LAPACK_zhecon_base LAPACK_GLOBAL(zhecon,ZHECON)
void LAPACK_zhecon_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double const* A, lapack_int const* lda, lapack_int const* ipiv,
    double const* anorm,
    double* rcond,
    lapack_complex_double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhecon(...) LAPACK_zhecon_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhecon(...) LAPACK_zhecon_base(__VA_ARGS__)
#endif

#define LAPACK_checon_3_base LAPACK_GLOBAL(checon_3,CHECON_3)
void LAPACK_checon_3_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float const* A, lapack_int const* lda,
    lapack_complex_float const* E, lapack_int const* ipiv,
    float const* anorm,
    float* rcond,
    lapack_complex_float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_checon_3(...) LAPACK_checon_3_base(__VA_ARGS__, 1)
#else
    #define LAPACK_checon_3(...) LAPACK_checon_3_base(__VA_ARGS__)
#endif

#define LAPACK_zhecon_3_base LAPACK_GLOBAL(zhecon_3,ZHECON_3)
void LAPACK_zhecon_3_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double const* A, lapack_int const* lda,
    lapack_complex_double const* E, lapack_int const* ipiv,
    double const* anorm,
    double* rcond,
    lapack_complex_double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhecon_3(...) LAPACK_zhecon_3_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhecon_3(...) LAPACK_zhecon_3_base(__VA_ARGS__)
#endif

#define LAPACK_cheequb_base LAPACK_GLOBAL(cheequb,CHEEQUB)
void LAPACK_cheequb_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float const* A, lapack_int const* lda,
    float* S,
    float* scond,
    float* amax,
    lapack_complex_float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cheequb(...) LAPACK_cheequb_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cheequb(...) LAPACK_cheequb_base(__VA_ARGS__)
#endif

#define LAPACK_zheequb_base LAPACK_GLOBAL(zheequb,ZHEEQUB)
void LAPACK_zheequb_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double const* A, lapack_int const* lda,
    double* S,
    double* scond,
    double* amax,
    lapack_complex_double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zheequb(...) LAPACK_zheequb_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zheequb(...) LAPACK_zheequb_base(__VA_ARGS__)
#endif

#define LAPACK_cheev_base LAPACK_GLOBAL(cheev,CHEEV)
void LAPACK_cheev_base(
    char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* W,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cheev(...) LAPACK_cheev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cheev(...) LAPACK_cheev_base(__VA_ARGS__)
#endif

#define LAPACK_zheev_base LAPACK_GLOBAL(zheev,ZHEEV)
void LAPACK_zheev_base(
    char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* W,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zheev(...) LAPACK_zheev_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zheev(...) LAPACK_zheev_base(__VA_ARGS__)
#endif

#define LAPACK_cheev_2stage_base LAPACK_GLOBAL(cheev_2stage,CHEEV_2STAGE)
void LAPACK_cheev_2stage_base(
    char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* W,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cheev_2stage(...) LAPACK_cheev_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cheev_2stage(...) LAPACK_cheev_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_zheev_2stage_base LAPACK_GLOBAL(zheev_2stage,ZHEEV_2STAGE)
void LAPACK_zheev_2stage_base(
    char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* W,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zheev_2stage(...) LAPACK_zheev_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zheev_2stage(...) LAPACK_zheev_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_cheevd_base LAPACK_GLOBAL(cheevd,CHEEVD)
void LAPACK_cheevd_base(
    char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* W,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cheevd(...) LAPACK_cheevd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cheevd(...) LAPACK_cheevd_base(__VA_ARGS__)
#endif

#define LAPACK_zheevd_base LAPACK_GLOBAL(zheevd,ZHEEVD)
void LAPACK_zheevd_base(
    char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* W,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zheevd(...) LAPACK_zheevd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zheevd(...) LAPACK_zheevd_base(__VA_ARGS__)
#endif

#define LAPACK_cheevd_2stage_base LAPACK_GLOBAL(cheevd_2stage,CHEEVD_2STAGE)
void LAPACK_cheevd_2stage_base(
    char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* W,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cheevd_2stage(...) LAPACK_cheevd_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cheevd_2stage(...) LAPACK_cheevd_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_zheevd_2stage_base LAPACK_GLOBAL(zheevd_2stage,ZHEEVD_2STAGE)
void LAPACK_zheevd_2stage_base(
    char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* W,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zheevd_2stage(...) LAPACK_zheevd_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zheevd_2stage(...) LAPACK_zheevd_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_cheevr_base LAPACK_GLOBAL(cheevr,CHEEVR)
void LAPACK_cheevr_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float const* vl,
    float const* vu, lapack_int const* il, lapack_int const* iu,
    float const* abstol, lapack_int* m,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz, lapack_int* ISUPPZ,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cheevr(...) LAPACK_cheevr_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cheevr(...) LAPACK_cheevr_base(__VA_ARGS__)
#endif

#define LAPACK_zheevr_base LAPACK_GLOBAL(zheevr,ZHEEVR)
void LAPACK_zheevr_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double const* vl,
    double const* vu, lapack_int const* il, lapack_int const* iu,
    double const* abstol, lapack_int* m,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz, lapack_int* ISUPPZ,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zheevr(...) LAPACK_zheevr_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zheevr(...) LAPACK_zheevr_base(__VA_ARGS__)
#endif

#define LAPACK_cheevr_2stage_base LAPACK_GLOBAL(cheevr_2stage,CHEEVR_2STAGE)
void LAPACK_cheevr_2stage_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float const* vl,
    float const* vu, lapack_int const* il, lapack_int const* iu,
    float const* abstol, lapack_int* m,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz, lapack_int* ISUPPZ,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cheevr_2stage(...) LAPACK_cheevr_2stage_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cheevr_2stage(...) LAPACK_cheevr_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_zheevr_2stage_base LAPACK_GLOBAL(zheevr_2stage,ZHEEVR_2STAGE)
void LAPACK_zheevr_2stage_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double const* vl,
    double const* vu, lapack_int const* il, lapack_int const* iu,
    double const* abstol, lapack_int* m,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz, lapack_int* ISUPPZ,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zheevr_2stage(...) LAPACK_zheevr_2stage_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zheevr_2stage(...) LAPACK_zheevr_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_cheevx_base LAPACK_GLOBAL(cheevx,CHEEVX)
void LAPACK_cheevx_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float const* vl,
    float const* vu, lapack_int const* il, lapack_int const* iu,
    float const* abstol, lapack_int* m,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cheevx(...) LAPACK_cheevx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cheevx(...) LAPACK_cheevx_base(__VA_ARGS__)
#endif

#define LAPACK_zheevx_base LAPACK_GLOBAL(zheevx,ZHEEVX)
void LAPACK_zheevx_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double const* vl,
    double const* vu, lapack_int const* il, lapack_int const* iu,
    double const* abstol, lapack_int* m,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zheevx(...) LAPACK_zheevx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zheevx(...) LAPACK_zheevx_base(__VA_ARGS__)
#endif

#define LAPACK_cheevx_2stage_base LAPACK_GLOBAL(cheevx_2stage,CHEEVX_2STAGE)
void LAPACK_cheevx_2stage_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float const* vl,
    float const* vu, lapack_int const* il, lapack_int const* iu,
    float const* abstol, lapack_int* m,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cheevx_2stage(...) LAPACK_cheevx_2stage_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_cheevx_2stage(...) LAPACK_cheevx_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_zheevx_2stage_base LAPACK_GLOBAL(zheevx_2stage,ZHEEVX_2STAGE)
void LAPACK_zheevx_2stage_base(
    char const* jobz, char const* range, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double const* vl,
    double const* vu, lapack_int const* il, lapack_int const* iu,
    double const* abstol, lapack_int* m,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zheevx_2stage(...) LAPACK_zheevx_2stage_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zheevx_2stage(...) LAPACK_zheevx_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_chegst_base LAPACK_GLOBAL(chegst,CHEGST)
void LAPACK_chegst_base(
    lapack_int const* itype, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    const lapack_complex_float* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chegst(...) LAPACK_chegst_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chegst(...) LAPACK_chegst_base(__VA_ARGS__)
#endif

#define LAPACK_zhegst_base LAPACK_GLOBAL(zhegst,ZHEGST)
void LAPACK_zhegst_base(
    lapack_int const* itype, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    const lapack_complex_double* B, lapack_int const* ldb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhegst(...) LAPACK_zhegst_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhegst(...) LAPACK_zhegst_base(__VA_ARGS__)
#endif

#define LAPACK_chegv_base LAPACK_GLOBAL(chegv,CHEGV)
void LAPACK_chegv_base(
    lapack_int const* itype, char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    float* W,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chegv(...) LAPACK_chegv_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chegv(...) LAPACK_chegv_base(__VA_ARGS__)
#endif

#define LAPACK_zhegv_base LAPACK_GLOBAL(zhegv,ZHEGV)
void LAPACK_zhegv_base(
    lapack_int const* itype, char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    double* W,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhegv(...) LAPACK_zhegv_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhegv(...) LAPACK_zhegv_base(__VA_ARGS__)
#endif

#define LAPACK_chegv_2stage_base LAPACK_GLOBAL(chegv_2stage,CHEGV_2STAGE)
void LAPACK_chegv_2stage_base(
    lapack_int const* itype, char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    float* W,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chegv_2stage(...) LAPACK_chegv_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chegv_2stage(...) LAPACK_chegv_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_zhegv_2stage_base LAPACK_GLOBAL(zhegv_2stage,ZHEGV_2STAGE)
void LAPACK_zhegv_2stage_base(
    lapack_int const* itype, char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    double* W,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhegv_2stage(...) LAPACK_zhegv_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhegv_2stage(...) LAPACK_zhegv_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_chegvd_base LAPACK_GLOBAL(chegvd,CHEGVD)
void LAPACK_chegvd_base(
    lapack_int const* itype, char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    float* W,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chegvd(...) LAPACK_chegvd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chegvd(...) LAPACK_chegvd_base(__VA_ARGS__)
#endif

#define LAPACK_zhegvd_base LAPACK_GLOBAL(zhegvd,ZHEGVD)
void LAPACK_zhegvd_base(
    lapack_int const* itype, char const* jobz, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    double* W,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork, lapack_int const* lrwork,
    lapack_int* iwork, lapack_int const* liwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhegvd(...) LAPACK_zhegvd_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhegvd(...) LAPACK_zhegvd_base(__VA_ARGS__)
#endif

#define LAPACK_chegvx_base LAPACK_GLOBAL(chegvx,CHEGVX)
void LAPACK_chegvx_base(
    lapack_int const* itype, char const* jobz, char const* range, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* B, lapack_int const* ldb,
    float const* vl,
    float const* vu, lapack_int const* il, lapack_int const* iu,
    float const* abstol, lapack_int* m,
    float* W,
    lapack_complex_float* Z, lapack_int const* ldz,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chegvx(...) LAPACK_chegvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_chegvx(...) LAPACK_chegvx_base(__VA_ARGS__)
#endif

#define LAPACK_zhegvx_base LAPACK_GLOBAL(zhegvx,ZHEGVX)
void LAPACK_zhegvx_base(
    lapack_int const* itype, char const* jobz, char const* range, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* B, lapack_int const* ldb,
    double const* vl,
    double const* vu, lapack_int const* il, lapack_int const* iu,
    double const* abstol, lapack_int* m,
    double* W,
    lapack_complex_double* Z, lapack_int const* ldz,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* iwork, lapack_int* IFAIL,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhegvx(...) LAPACK_zhegvx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zhegvx(...) LAPACK_zhegvx_base(__VA_ARGS__)
#endif

#define LAPACK_cherfs_base LAPACK_GLOBAL(cherfs,CHERFS)
void LAPACK_cherfs_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float const* A, lapack_int const* lda,
    lapack_complex_float const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    lapack_complex_float const* B, lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* ferr,
    float* berr,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cherfs(...) LAPACK_cherfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cherfs(...) LAPACK_cherfs_base(__VA_ARGS__)
#endif

#define LAPACK_zherfs_base LAPACK_GLOBAL(zherfs,ZHERFS)
void LAPACK_zherfs_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double const* A, lapack_int const* lda,
    lapack_complex_double const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    lapack_complex_double const* B, lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* ferr,
    double* berr,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zherfs(...) LAPACK_zherfs_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zherfs(...) LAPACK_zherfs_base(__VA_ARGS__)
#endif

#define LAPACK_cherfsx_base LAPACK_GLOBAL(cherfsx,CHERFSX)
void LAPACK_cherfsx_base(
    char const* uplo, char const* equed,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float const* A, lapack_int const* lda,
    lapack_complex_float const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    const float* S,
    lapack_complex_float const* B, lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* rcond,
    float* berr, lapack_int const* n_err_bnds,
    float* err_bnds_norm,
    float* err_bnds_comp, lapack_int const* nparams,
    float* params,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cherfsx(...) LAPACK_cherfsx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_cherfsx(...) LAPACK_cherfsx_base(__VA_ARGS__)
#endif

#define LAPACK_zherfsx_base LAPACK_GLOBAL(zherfsx,ZHERFSX)
void LAPACK_zherfsx_base(
    char const* uplo, char const* equed,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double const* A, lapack_int const* lda,
    lapack_complex_double const* AF, lapack_int const* ldaf, lapack_int const* ipiv,
    const double* S,
    lapack_complex_double const* B, lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* rcond,
    double* berr, lapack_int const* n_err_bnds,
    double* err_bnds_norm,
    double* err_bnds_comp, lapack_int const* nparams,
    double* params,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zherfsx(...) LAPACK_zherfsx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zherfsx(...) LAPACK_zherfsx_base(__VA_ARGS__)
#endif

#define LAPACK_chesv_base LAPACK_GLOBAL(chesv,CHESV)
void LAPACK_chesv_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chesv(...) LAPACK_chesv_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chesv(...) LAPACK_chesv_base(__VA_ARGS__)
#endif

#define LAPACK_zhesv_base LAPACK_GLOBAL(zhesv,ZHESV)
void LAPACK_zhesv_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhesv(...) LAPACK_zhesv_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhesv(...) LAPACK_zhesv_base(__VA_ARGS__)
#endif

#define LAPACK_chesv_aa_base LAPACK_GLOBAL(chesv_aa,CHESV_AA)
void LAPACK_chesv_aa_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chesv_aa(...) LAPACK_chesv_aa_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chesv_aa(...) LAPACK_chesv_aa_base(__VA_ARGS__)
#endif

#define LAPACK_zhesv_aa_base LAPACK_GLOBAL(zhesv_aa,ZHESV_AA)
void LAPACK_zhesv_aa_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhesv_aa(...) LAPACK_zhesv_aa_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhesv_aa(...) LAPACK_zhesv_aa_base(__VA_ARGS__)
#endif

#define LAPACK_chesv_aa_2stage_base LAPACK_GLOBAL(chesv_aa_2stage,CHESV_AA_2STAGE)
void LAPACK_chesv_aa_2stage_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* TB, lapack_int const* ltb, lapack_int* ipiv, lapack_int* ipiv2,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chesv_aa_2stage(...) LAPACK_chesv_aa_2stage_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chesv_aa_2stage(...) LAPACK_chesv_aa_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_zhesv_aa_2stage_base LAPACK_GLOBAL(zhesv_aa_2stage,ZHESV_AA_2STAGE)
void LAPACK_zhesv_aa_2stage_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* TB, lapack_int const* ltb, lapack_int* ipiv, lapack_int* ipiv2,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhesv_aa_2stage(...) LAPACK_zhesv_aa_2stage_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhesv_aa_2stage(...) LAPACK_zhesv_aa_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_chesv_rk_base LAPACK_GLOBAL(chesv_rk,CHESV_RK)
void LAPACK_chesv_rk_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* E, lapack_int* ipiv,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chesv_rk(...) LAPACK_chesv_rk_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chesv_rk(...) LAPACK_chesv_rk_base(__VA_ARGS__)
#endif

#define LAPACK_zhesv_rk_base LAPACK_GLOBAL(zhesv_rk,ZHESV_RK)
void LAPACK_zhesv_rk_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* E, lapack_int* ipiv,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhesv_rk(...) LAPACK_zhesv_rk_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhesv_rk(...) LAPACK_zhesv_rk_base(__VA_ARGS__)
#endif

#define LAPACK_chesv_rook_base LAPACK_GLOBAL(chesv_rook,CHESV_ROOK)
void LAPACK_chesv_rook_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_float* B, lapack_int const* ldb,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chesv_rook(...) LAPACK_chesv_rook_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chesv_rook(...) LAPACK_chesv_rook_base(__VA_ARGS__)
#endif

#define LAPACK_zhesv_rook_base LAPACK_GLOBAL(zhesv_rook,ZHESV_ROOK)
void LAPACK_zhesv_rook_base(
    char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_double* B, lapack_int const* ldb,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhesv_rook(...) LAPACK_zhesv_rook_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhesv_rook(...) LAPACK_zhesv_rook_base(__VA_ARGS__)
#endif

#define LAPACK_chesvx_base LAPACK_GLOBAL(chesvx,CHESVX)
void LAPACK_chesvx_base(
    char const* fact, char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float const* A, lapack_int const* lda,
    lapack_complex_float* AF, lapack_int const* ldaf, lapack_int* ipiv,
    lapack_complex_float const* B, lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* rcond,
    float* ferr,
    float* berr,
    lapack_complex_float* work, lapack_int const* lwork,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chesvx(...) LAPACK_chesvx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chesvx(...) LAPACK_chesvx_base(__VA_ARGS__)
#endif

#define LAPACK_zhesvx_base LAPACK_GLOBAL(zhesvx,ZHESVX)
void LAPACK_zhesvx_base(
    char const* fact, char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double const* A, lapack_int const* lda,
    lapack_complex_double* AF, lapack_int const* ldaf, lapack_int* ipiv,
    lapack_complex_double const* B, lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* rcond,
    double* ferr,
    double* berr,
    lapack_complex_double* work, lapack_int const* lwork,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhesvx(...) LAPACK_zhesvx_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhesvx(...) LAPACK_zhesvx_base(__VA_ARGS__)
#endif

#define LAPACK_chesvxx_base LAPACK_GLOBAL(chesvxx,CHESVXX)
void LAPACK_chesvxx_base(
    char const* fact, char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* AF, lapack_int const* ldaf, lapack_int* ipiv, char* equed,
    float* S,
    lapack_complex_float* B,
    lapack_int const* ldb,
    lapack_complex_float* X, lapack_int const* ldx,
    float* rcond,
    float* rpvgrw,
    float* berr, lapack_int const* n_err_bnds,
    float* err_bnds_norm,
    float* err_bnds_comp, lapack_int const* nparams,
    float* params,
    lapack_complex_float* work,
    float* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chesvxx(...) LAPACK_chesvxx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_chesvxx(...) LAPACK_chesvxx_base(__VA_ARGS__)
#endif

#define LAPACK_zhesvxx_base LAPACK_GLOBAL(zhesvxx,ZHESVXX)
void LAPACK_zhesvxx_base(
    char const* fact, char const* uplo,
    lapack_int const* n, lapack_int const* nrhs,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* AF, lapack_int const* ldaf, lapack_int* ipiv, char* equed,
    double* S,
    lapack_complex_double* B,
    lapack_int const* ldb,
    lapack_complex_double* X, lapack_int const* ldx,
    double* rcond,
    double* rpvgrw,
    double* berr, lapack_int const* n_err_bnds,
    double* err_bnds_norm,
    double* err_bnds_comp, lapack_int const* nparams,
    double* params,
    lapack_complex_double* work,
    double* rwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhesvxx(...) LAPACK_zhesvxx_base(__VA_ARGS__, 1, 1, 1)
#else
    #define LAPACK_zhesvxx(...) LAPACK_zhesvxx_base(__VA_ARGS__)
#endif

#define LAPACK_cheswapr_base LAPACK_GLOBAL(cheswapr,CHESWAPR)
void LAPACK_cheswapr_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int const* i1, lapack_int const* i2
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_cheswapr(...) LAPACK_cheswapr_base(__VA_ARGS__, 1)
#else
    #define LAPACK_cheswapr(...) LAPACK_cheswapr_base(__VA_ARGS__)
#endif

#define LAPACK_zheswapr_base LAPACK_GLOBAL(zheswapr,ZHESWAPR)
void LAPACK_zheswapr_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int const* i1, lapack_int const* i2
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zheswapr(...) LAPACK_zheswapr_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zheswapr(...) LAPACK_zheswapr_base(__VA_ARGS__)
#endif

#define LAPACK_chetrd_base LAPACK_GLOBAL(chetrd,CHETRD)
void LAPACK_chetrd_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* D,
    float* E,
    lapack_complex_float* tau,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chetrd(...) LAPACK_chetrd_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chetrd(...) LAPACK_chetrd_base(__VA_ARGS__)
#endif

#define LAPACK_zhetrd_base LAPACK_GLOBAL(zhetrd,ZHETRD)
void LAPACK_zhetrd_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* D,
    double* E,
    lapack_complex_double* tau,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhetrd(...) LAPACK_zhetrd_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhetrd(...) LAPACK_zhetrd_base(__VA_ARGS__)
#endif

#define LAPACK_chetrd_2stage_base LAPACK_GLOBAL(chetrd_2stage,CHETRD_2STAGE)
void LAPACK_chetrd_2stage_base(
    char const* vect, char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    float* D,
    float* E,
    lapack_complex_float* tau,
    lapack_complex_float* HOUS2, lapack_int const* lhous2,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chetrd_2stage(...) LAPACK_chetrd_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_chetrd_2stage(...) LAPACK_chetrd_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_zhetrd_2stage_base LAPACK_GLOBAL(zhetrd_2stage,ZHETRD_2STAGE)
void LAPACK_zhetrd_2stage_base(
    char const* vect, char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    double* D,
    double* E,
    lapack_complex_double* tau,
    lapack_complex_double* HOUS2, lapack_int const* lhous2,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t, size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhetrd_2stage(...) LAPACK_zhetrd_2stage_base(__VA_ARGS__, 1, 1)
#else
    #define LAPACK_zhetrd_2stage(...) LAPACK_zhetrd_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_chetrf_base LAPACK_GLOBAL(chetrf,CHETRF)
void LAPACK_chetrf_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chetrf(...) LAPACK_chetrf_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chetrf(...) LAPACK_chetrf_base(__VA_ARGS__)
#endif

#define LAPACK_zhetrf_base LAPACK_GLOBAL(zhetrf,ZHETRF)
void LAPACK_zhetrf_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhetrf(...) LAPACK_zhetrf_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhetrf(...) LAPACK_zhetrf_base(__VA_ARGS__)
#endif

#define LAPACK_chetrf_aa_base LAPACK_GLOBAL(chetrf_aa,CHETRF_AA)
void LAPACK_chetrf_aa_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chetrf_aa(...) LAPACK_chetrf_aa_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chetrf_aa(...) LAPACK_chetrf_aa_base(__VA_ARGS__)
#endif

#define LAPACK_zhetrf_aa_base LAPACK_GLOBAL(zhetrf_aa,ZHETRF_AA)
void LAPACK_zhetrf_aa_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhetrf_aa(...) LAPACK_zhetrf_aa_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhetrf_aa(...) LAPACK_zhetrf_aa_base(__VA_ARGS__)
#endif

#define LAPACK_chetrf_aa_2stage_base LAPACK_GLOBAL(chetrf_aa_2stage,CHETRF_AA_2STAGE)
void LAPACK_chetrf_aa_2stage_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* TB, lapack_int const* ltb, lapack_int* ipiv, lapack_int* ipiv2,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chetrf_aa_2stage(...) LAPACK_chetrf_aa_2stage_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chetrf_aa_2stage(...) LAPACK_chetrf_aa_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_zhetrf_aa_2stage_base LAPACK_GLOBAL(zhetrf_aa_2stage,ZHETRF_AA_2STAGE)
void LAPACK_zhetrf_aa_2stage_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* TB, lapack_int const* ltb, lapack_int* ipiv, lapack_int* ipiv2,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhetrf_aa_2stage(...) LAPACK_zhetrf_aa_2stage_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhetrf_aa_2stage(...) LAPACK_zhetrf_aa_2stage_base(__VA_ARGS__)
#endif

#define LAPACK_chetrf_rk_base LAPACK_GLOBAL(chetrf_rk,CHETRF_RK)
void LAPACK_chetrf_rk_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float* E, lapack_int* ipiv,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chetrf_rk(...) LAPACK_chetrf_rk_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chetrf_rk(...) LAPACK_chetrf_rk_base(__VA_ARGS__)
#endif

#define LAPACK_zhetrf_rk_base LAPACK_GLOBAL(zhetrf_rk,ZHETRF_RK)
void LAPACK_zhetrf_rk_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda,
    lapack_complex_double* E, lapack_int* ipiv,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhetrf_rk(...) LAPACK_zhetrf_rk_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhetrf_rk(...) LAPACK_zhetrf_rk_base(__VA_ARGS__)
#endif

#define LAPACK_chetrf_rook_base LAPACK_GLOBAL(chetrf_rook,CHETRF_ROOK)
void LAPACK_chetrf_rook_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chetrf_rook(...) LAPACK_chetrf_rook_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chetrf_rook(...) LAPACK_chetrf_rook_base(__VA_ARGS__)
#endif

#define LAPACK_zhetrf_rook_base LAPACK_GLOBAL(zhetrf_rook,ZHETRF_ROOK)
void LAPACK_zhetrf_rook_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int* ipiv,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhetrf_rook(...) LAPACK_zhetrf_rook_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhetrf_rook(...) LAPACK_zhetrf_rook_base(__VA_ARGS__)
#endif

#define LAPACK_chetri_base LAPACK_GLOBAL(chetri,CHETRI)
void LAPACK_chetri_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int const* ipiv,
    lapack_complex_float* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chetri(...) LAPACK_chetri_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chetri(...) LAPACK_chetri_base(__VA_ARGS__)
#endif

#define LAPACK_zhetri_base LAPACK_GLOBAL(zhetri,ZHETRI)
void LAPACK_zhetri_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int const* ipiv,
    lapack_complex_double* work,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhetri(...) LAPACK_zhetri_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhetri(...) LAPACK_zhetri_base(__VA_ARGS__)
#endif

#define LAPACK_chetri2_base LAPACK_GLOBAL(chetri2,CHETRI2)
void LAPACK_chetri2_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int const* ipiv,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chetri2(...) LAPACK_chetri2_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chetri2(...) LAPACK_chetri2_base(__VA_ARGS__)
#endif

#define LAPACK_zhetri2_base LAPACK_GLOBAL(zhetri2,ZHETRI2)
void LAPACK_zhetri2_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int const* ipiv,
    lapack_complex_double* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhetri2(...) LAPACK_zhetri2_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhetri2(...) LAPACK_zhetri2_base(__VA_ARGS__)
#endif

#define LAPACK_chetri2x_base LAPACK_GLOBAL(chetri2x,CHETRI2X)
void LAPACK_chetri2x_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda, lapack_int const* ipiv,
    lapack_complex_float* work, lapack_int const* nb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chetri2x(...) LAPACK_chetri2x_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chetri2x(...) LAPACK_chetri2x_base(__VA_ARGS__)
#endif

#define LAPACK_zhetri2x_base LAPACK_GLOBAL(zhetri2x,ZHETRI2X)
void LAPACK_zhetri2x_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_double* A, lapack_int const* lda, lapack_int const* ipiv,
    lapack_complex_double* work, lapack_int const* nb,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_zhetri2x(...) LAPACK_zhetri2x_base(__VA_ARGS__, 1)
#else
    #define LAPACK_zhetri2x(...) LAPACK_zhetri2x_base(__VA_ARGS__)
#endif

#define LAPACK_chetri_3_base LAPACK_GLOBAL(chetri_3,CHETRI_3)
void LAPACK_chetri_3_base(
    char const* uplo,
    lapack_int const* n,
    lapack_complex_float* A, lapack_int const* lda,
    lapack_complex_float const* E, lapack_int const* ipiv,
    lapack_complex_float* work, lapack_int const* lwork,
    lapack_int* info
#ifdef LAPACK_FORTRAN_STRLEN_END
    , size_t
#endif
);
#ifdef LAPACK_FORTRAN_STRLEN_END
    #define LAPACK_chetri_3(...) LAPACK_chetri_3_base(__VA_ARGS__, 1)
#else
    #define LAPACK_chetri_3(...) LAPACK_chetri_3_base(__VA_ARGS__)
#endif

#define LAPACK_zhetri_3_base LAPACK_GLOBAL(zhetri_3,ZHETRI_3)
void LAPACK_zhetri_3_ba
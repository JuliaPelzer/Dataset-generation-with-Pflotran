/*****************************************************************************
  Copyright (c) 2014, Intel Corp.
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Intel Corporation nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
  THE POSSIBILITY OF SUCH DAMAGE.
******************************************************************************
* Contents: Native C interface to LAPACK
* Author: Intel Corporation
*****************************************************************************/

#ifndef _LAPACKE_H_
#define _LAPACKE_H_

#include "lapack.h"

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#ifndef LAPACKE_malloc
#define LAPACKE_malloc( size ) malloc( size )
#endif
#ifndef LAPACKE_free
#define LAPACKE_free( p )      free( p )
#endif

#define LAPACK_C2INT( x ) (lapack_int)(*((float*)&x ))
#define LAPACK_Z2INT( x ) (lapack_int)(*((double*)&x ))

#define LAPACK_ROW_MAJOR               101
#define LAPACK_COL_MAJOR               102

#define LAPACK_WORK_MEMORY_ERROR       -1010
#define LAPACK_TRANSPOSE_MEMORY_ERROR  -1011

lapack_complex_float lapack_make_complex_float( float re, float im );
lapack_complex_double lapack_make_complex_double( double re, double im );

/* C-LAPACK function prototypes */

lapack_int LAPACKE_sbdsdc( int matrix_layout, char uplo, char compq,
                           lapack_int n, float* d, float* e, float* u,
                           lapack_int ldu, float* vt, lapack_int ldvt, float* q,
                           lapack_int* iq );
lapack_int LAPACKE_dbdsdc( int matrix_layout, char uplo, char compq,
                           lapack_int n, double* d, double* e, double* u,
                           lapack_int ldu, double* vt, lapack_int ldvt,
                           double* q, lapack_int* iq );

lapack_int LAPACKE_sbdsqr( int matrix_layout, char uplo, lapack_int n,
                           lapack_int ncvt, lapack_int nru, lapack_int ncc,
                           float* d, float* e, float* vt, lapack_int ldvt,
                           float* u, lapack_int ldu, float* c, lapack_int ldc );
lapack_int LAPACKE_dbdsqr( int matrix_layout, char uplo, lapack_int n,
                           lapack_int ncvt, lapack_int nru, lapack_int ncc,
                           double* d, double* e, double* vt, lapack_int ldvt,
                           double* u, lapack_int ldu, double* c,
                           lapack_int ldc );
lapack_int LAPACKE_cbdsqr( int matrix_layout, char uplo, lapack_int n,
                           lapack_int ncvt, lapack_int nru, lapack_int ncc,
                           float* d, float* e, lapack_complex_float* vt,
                           lapack_int ldvt, lapack_complex_float* u,
                           lapack_int ldu, lapack_complex_float* c,
                           lapack_int ldc );
lapack_int LAPACKE_zbdsqr( int matrix_layout, char uplo, lapack_int n,
                           lapack_int ncvt, lapack_int nru, lapack_int ncc,
                           double* d, double* e, lapack_complex_double* vt,
                           lapack_int ldvt, lapack_complex_double* u,
                           lapack_int ldu, lapack_complex_double* c,
                           lapack_int ldc );
lapack_int LAPACKE_sbdsvdx( int matrix_layout, char uplo, char jobz, char range,
                           lapack_int n, float* d, float* e,
                           float vl, float vu,
                           lapack_int il, lapack_int iu, lapack_int* ns,
                           float* s, float* z, lapack_int ldz,
                           lapack_int* superb );
lapack_int LAPACKE_dbdsvdx( int matrix_layout, char uplo, char jobz, char range,
                           lapack_int n, double* d, double* e,
                           double vl, double vu,
                           lapack_int il, lapack_int iu, lapack_int* ns,
                           double* s, double* z, lapack_int ldz,
                           lapack_int* superb );
lapack_int LAPACKE_sdisna( char job, lapack_int m, lapack_int n, const float* d,
                           float* sep );
lapack_int LAPACKE_ddisna( char job, lapack_int m, lapack_int n,
                           const double* d, double* sep );

lapack_int LAPACKE_sgbbrd( int matrix_layout, char vect, lapack_int m,
                           lapack_int n, lapack_int ncc, lapack_int kl,
                           lapack_int ku, float* ab, lapack_int ldab, float* d,
                           float* e, float* q, lapack_int ldq, float* pt,
                           lapack_int ldpt, float* c, lapack_int ldc );
lapack_int LAPACKE_dgbbrd( int matrix_layout, char vect, lapack_int m,
                           lapack_int n, lapack_int ncc, lapack_int kl,
                           lapack_int ku, double* ab, lapack_int ldab,
                           double* d, double* e, double* q, lapack_int ldq,
                           double* pt, lapack_int ldpt, double* c,
                           lapack_int ldc );
lapack_int LAPACKE_cgbbrd( int matrix_layout, char vect, lapack_int m,
                           lapack_int n, lapack_int ncc, lapack_int kl,
                           lapack_int ku, lapack_complex_float* ab,
                           lapack_int ldab, float* d, float* e,
                           lapack_complex_float* q, lapack_int ldq,
                           lapack_complex_float* pt, lapack_int ldpt,
                           lapack_complex_float* c, lapack_int ldc );
lapack_int LAPACKE_zgbbrd( int matrix_layout, char vect, lapack_int m,
                           lapack_int n, lapack_int ncc, lapack_int kl,
                           lapack_int ku, lapack_complex_double* ab,
                           lapack_int ldab, double* d, double* e,
                           lapack_complex_double* q, lapack_int ldq,
                           lapack_complex_double* pt, lapack_int ldpt,
                           lapack_complex_double* c, lapack_int ldc );

lapack_int LAPACKE_sgbcon( int matrix_layout, char norm, lapack_int n,
                           lapack_int kl, lapack_int ku, const float* ab,
                           lapack_int ldab, const lapack_int* ipiv, float anorm,
                           float* rcond );
lapack_int LAPACKE_dgbcon( int matrix_layout, char norm, lapack_int n,
                           lapack_int kl, lapack_int ku, const double* ab,
                           lapack_int ldab, const lapack_int* ipiv,
                           double anorm, double* rcond );
lapack_int LAPACKE_cgbcon( int matrix_layout, char norm, lapack_int n,
                           lapack_int kl, lapack_int ku,
                           const lapack_complex_float* ab, lapack_int ldab,
                           const lapack_int* ipiv, float anorm, float* rcond );
lapack_int LAPACKE_zgbcon( int matrix_layout, char norm, lapack_int n,
                           lapack_int kl, lapack_int ku,
                           const lapack_complex_double* ab, lapack_int ldab,
                           const lapack_int* ipiv, double anorm,
                           double* rcond );

lapack_int LAPACKE_sgbequ( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku, const float* ab,
                           lapack_int ldab, float* r, float* c, float* rowcnd,
                           float* colcnd, float* amax );
lapack_int LAPACKE_dgbequ( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku, const double* ab,
                           lapack_int ldab, double* r, double* c,
                           double* rowcnd, double* colcnd, double* amax );
lapack_int LAPACKE_cgbequ( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku,
                           const lapack_complex_float* ab, lapack_int ldab,
                           float* r, float* c, float* rowcnd, float* colcnd,
                           float* amax );
lapack_int LAPACKE_zgbequ( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku,
                           const lapack_complex_double* ab, lapack_int ldab,
                           double* r, double* c, double* rowcnd, double* colcnd,
                           double* amax );

lapack_int LAPACKE_sgbequb( int matrix_layout, lapack_int m, lapack_int n,
                            lapack_int kl, lapack_int ku, const float* ab,
                            lapack_int ldab, float* r, float* c, float* rowcnd,
                            float* colcnd, float* amax );
lapack_int LAPACKE_dgbequb( int matrix_layout, lapack_int m, lapack_int n,
                            lapack_int kl, lapack_int ku, const double* ab,
                            lapack_int ldab, double* r, double* c,
                            double* rowcnd, double* colcnd, double* amax );
lapack_int LAPACKE_cgbequb( int matrix_layout, lapack_int m, lapack_int n,
                            lapack_int kl, lapack_int ku,
                            const lapack_complex_float* ab, lapack_int ldab,
                            float* r, float* c, float* rowcnd, float* colcnd,
                            float* amax );
lapack_int LAPACKE_zgbequb( int matrix_layout, lapack_int m, lapack_int n,
                            lapack_int kl, lapack_int ku,
                            const lapack_complex_double* ab, lapack_int ldab,
                            double* r, double* c, double* rowcnd,
                            double* colcnd, double* amax );

lapack_int LAPACKE_sgbrfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int kl, lapack_int ku, lapack_int nrhs,
                           const float* ab, lapack_int ldab, const float* afb,
                           lapack_int ldafb, const lapack_int* ipiv,
                           const float* b, lapack_int ldb, float* x,
                           lapack_int ldx, float* ferr, float* berr );
lapack_int LAPACKE_dgbrfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int kl, lapack_int ku, lapack_int nrhs,
                           const double* ab, lapack_int ldab, const double* afb,
                           lapack_int ldafb, const lapack_int* ipiv,
                           const double* b, lapack_int ldb, double* x,
                           lapack_int ldx, double* ferr, double* berr );
lapack_int LAPACKE_cgbrfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int kl, lapack_int ku, lapack_int nrhs,
                           const lapack_complex_float* ab, lapack_int ldab,
                           const lapack_complex_float* afb, lapack_int ldafb,
                           const lapack_int* ipiv,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx, float* ferr,
                           float* berr );
lapack_int LAPACKE_zgbrfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int kl, lapack_int ku, lapack_int nrhs,
                           const lapack_complex_double* ab, lapack_int ldab,
                           const lapack_complex_double* afb, lapack_int ldafb,
                           const lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* ferr, double* berr );

lapack_int LAPACKE_sgbrfsx( int matrix_layout, char trans, char equed,
                            lapack_int n, lapack_int kl, lapack_int ku,
                            lapack_int nrhs, const float* ab, lapack_int ldab,
                            const float* afb, lapack_int ldafb,
                            const lapack_int* ipiv, const float* r,
                            const float* c, const float* b, lapack_int ldb,
                            float* x, lapack_int ldx, float* rcond, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_dgbrfsx( int matrix_layout, char trans, char equed,
                            lapack_int n, lapack_int kl, lapack_int ku,
                            lapack_int nrhs, const double* ab, lapack_int ldab,
                            const double* afb, lapack_int ldafb,
                            const lapack_int* ipiv, const double* r,
                            const double* c, const double* b, lapack_int ldb,
                            double* x, lapack_int ldx, double* rcond,
                            double* berr, lapack_int n_err_bnds,
                            double* err_bnds_norm, double* err_bnds_comp,
                            lapack_int nparams, double* params );
lapack_int LAPACKE_cgbrfsx( int matrix_layout, char trans, char equed,
                            lapack_int n, lapack_int kl, lapack_int ku,
                            lapack_int nrhs, const lapack_complex_float* ab,
                            lapack_int ldab, const lapack_complex_float* afb,
                            lapack_int ldafb, const lapack_int* ipiv,
                            const float* r, const float* c,
                            const lapack_complex_float* b, lapack_int ldb,
                            lapack_complex_float* x, lapack_int ldx,
                            float* rcond, float* berr, lapack_int n_err_bnds,
                            float* err_bnds_norm, float* err_bnds_comp,
                            lapack_int nparams, float* params );
lapack_int LAPACKE_zgbrfsx( int matrix_layout, char trans, char equed,
                            lapack_int n, lapack_int kl, lapack_int ku,
                            lapack_int nrhs, const lapack_complex_double* ab,
                            lapack_int ldab, const lapack_complex_double* afb,
                            lapack_int ldafb, const lapack_int* ipiv,
                            const double* r, const double* c,
                            const lapack_complex_double* b, lapack_int ldb,
                            lapack_complex_double* x, lapack_int ldx,
                            double* rcond, double* berr, lapack_int n_err_bnds,
                            double* err_bnds_norm, double* err_bnds_comp,
                            lapack_int nparams, double* params );

lapack_int LAPACKE_sgbsv( int matrix_layout, lapack_int n, lapack_int kl,
                          lapack_int ku, lapack_int nrhs, float* ab,
                          lapack_int ldab, lapack_int* ipiv, float* b,
                          lapack_int ldb );
lapack_int LAPACKE_dgbsv( int matrix_layout, lapack_int n, lapack_int kl,
                          lapack_int ku, lapack_int nrhs, double* ab,
                          lapack_int ldab, lapack_int* ipiv, double* b,
                          lapack_int ldb );
lapack_int LAPACKE_cgbsv( int matrix_layout, lapack_int n, lapack_int kl,
                          lapack_int ku, lapack_int nrhs,
                          lapack_complex_float* ab, lapack_int ldab,
                          lapack_int* ipiv, lapack_complex_float* b,
                          lapack_int ldb );
lapack_int LAPACKE_zgbsv( int matrix_layout, lapack_int n, lapack_int kl,
                          lapack_int ku, lapack_int nrhs,
                          lapack_complex_double* ab, lapack_int ldab,
                          lapack_int* ipiv, lapack_complex_double* b,
                          lapack_int ldb );

lapack_int LAPACKE_sgbsvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int kl, lapack_int ku,
                           lapack_int nrhs, float* ab, lapack_int ldab,
                           float* afb, lapack_int ldafb, lapack_int* ipiv,
                           char* equed, float* r, float* c, float* b,
                           lapack_int ldb, float* x, lapack_int ldx,
                           float* rcond, float* ferr, float* berr,
                           float* rpivot );
lapack_int LAPACKE_dgbsvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int kl, lapack_int ku,
                           lapack_int nrhs, double* ab, lapack_int ldab,
                           double* afb, lapack_int ldafb, lapack_int* ipiv,
                           char* equed, double* r, double* c, double* b,
                           lapack_int ldb, double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr,
                           double* rpivot );
lapack_int LAPACKE_cgbsvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int kl, lapack_int ku,
                           lapack_int nrhs, lapack_complex_float* ab,
                           lapack_int ldab, lapack_complex_float* afb,
                           lapack_int ldafb, lapack_int* ipiv, char* equed,
                           float* r, float* c, lapack_complex_float* b,
                           lapack_int ldb, lapack_complex_float* x,
                           lapack_int ldx, float* rcond, float* ferr,
                           float* berr, float* rpivot );
lapack_int LAPACKE_zgbsvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int kl, lapack_int ku,
                           lapack_int nrhs, lapack_complex_double* ab,
                           lapack_int ldab, lapack_complex_double* afb,
                           lapack_int ldafb, lapack_int* ipiv, char* equed,
                           double* r, double* c, lapack_complex_double* b,
                           lapack_int ldb, lapack_complex_double* x,
                           lapack_int ldx, double* rcond, double* ferr,
                           double* berr, double* rpivot );

lapack_int LAPACKE_sgbsvxx( int matrix_layout, char fact, char trans,
                            lapack_int n, lapack_int kl, lapack_int ku,
                            lapack_int nrhs, float* ab, lapack_int ldab,
                            float* afb, lapack_int ldafb, lapack_int* ipiv,
                            char* equed, float* r, float* c, float* b,
                            lapack_int ldb, float* x, lapack_int ldx,
                            float* rcond, float* rpvgrw, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_dgbsvxx( int matrix_layout, char fact, char trans,
                            lapack_int n, lapack_int kl, lapack_int ku,
                            lapack_int nrhs, double* ab, lapack_int ldab,
                            double* afb, lapack_int ldafb, lapack_int* ipiv,
                            char* equed, double* r, double* c, double* b,
                            lapack_int ldb, double* x, lapack_int ldx,
                            double* rcond, double* rpvgrw, double* berr,
                            lapack_int n_err_bnds, double* err_bnds_norm,
                            double* err_bnds_comp, lapack_int nparams,
                            double* params );
lapack_int LAPACKE_cgbsvxx( int matrix_layout, char fact, char trans,
                            lapack_int n, lapack_int kl, lapack_int ku,
                            lapack_int nrhs, lapack_complex_float* ab,
                            lapack_int ldab, lapack_complex_float* afb,
                            lapack_int ldafb, lapack_int* ipiv, char* equed,
                            float* r, float* c, lapack_complex_float* b,
                            lapack_int ldb, lapack_complex_float* x,
                            lapack_int ldx, float* rcond, float* rpvgrw,
                            float* berr, lapack_int n_err_bnds,
                            float* err_bnds_norm, float* err_bnds_comp,
                            lapack_int nparams, float* params );
lapack_int LAPACKE_zgbsvxx( int matrix_layout, char fact, char trans,
                            lapack_int n, lapack_int kl, lapack_int ku,
                            lapack_int nrhs, lapack_complex_double* ab,
                            lapack_int ldab, lapack_complex_double* afb,
                            lapack_int ldafb, lapack_int* ipiv, char* equed,
                            double* r, double* c, lapack_complex_double* b,
                            lapack_int ldb, lapack_complex_double* x,
                            lapack_int ldx, double* rcond, double* rpvgrw,
                            double* berr, lapack_int n_err_bnds,
                            double* err_bnds_norm, double* err_bnds_comp,
                            lapack_int nparams, double* params );

lapack_int LAPACKE_sgbtrf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku, float* ab,
                           lapack_int ldab, lapack_int* ipiv );
lapack_int LAPACKE_dgbtrf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku, double* ab,
                           lapack_int ldab, lapack_int* ipiv );
lapack_int LAPACKE_cgbtrf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku,
                           lapack_complex_float* ab, lapack_int ldab,
                           lapack_int* ipiv );
lapack_int LAPACKE_zgbtrf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku,
                           lapack_complex_double* ab, lapack_int ldab,
                           lapack_int* ipiv );

lapack_int LAPACKE_sgbtrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int kl, lapack_int ku, lapack_int nrhs,
                           const float* ab, lapack_int ldab,
                           const lapack_int* ipiv, float* b, lapack_int ldb );
lapack_int LAPACKE_dgbtrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int kl, lapack_int ku, lapack_int nrhs,
                           const double* ab, lapack_int ldab,
                           const lapack_int* ipiv, double* b, lapack_int ldb );
lapack_int LAPACKE_cgbtrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int kl, lapack_int ku, lapack_int nrhs,
                           const lapack_complex_float* ab, lapack_int ldab,
                           const lapack_int* ipiv, lapack_complex_float* b,
                           lapack_int ldb );
lapack_int LAPACKE_zgbtrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int kl, lapack_int ku, lapack_int nrhs,
                           const lapack_complex_double* ab, lapack_int ldab,
                           const lapack_int* ipiv, lapack_complex_double* b,
                           lapack_int ldb );

lapack_int LAPACKE_sgebak( int matrix_layout, char job, char side, lapack_int n,
                           lapack_int ilo, lapack_int ihi, const float* scale,
                           lapack_int m, float* v, lapack_int ldv );
lapack_int LAPACKE_dgebak( int matrix_layout, char job, char side, lapack_int n,
                           lapack_int ilo, lapack_int ihi, const double* scale,
                           lapack_int m, double* v, lapack_int ldv );
lapack_int LAPACKE_cgebak( int matrix_layout, char job, char side, lapack_int n,
                           lapack_int ilo, lapack_int ihi, const float* scale,
                           lapack_int m, lapack_complex_float* v,
                           lapack_int ldv );
lapack_int LAPACKE_zgebak( int matrix_layout, char job, char side, lapack_int n,
                           lapack_int ilo, lapack_int ihi, const double* scale,
                           lapack_int m, lapack_complex_double* v,
                           lapack_int ldv );

lapack_int LAPACKE_sgebal( int matrix_layout, char job, lapack_int n, float* a,
                           lapack_int lda, lapack_int* ilo, lapack_int* ihi,
                           float* scale );
lapack_int LAPACKE_dgebal( int matrix_layout, char job, lapack_int n, double* a,
                           lapack_int lda, lapack_int* ilo, lapack_int* ihi,
                           double* scale );
lapack_int LAPACKE_cgebal( int matrix_layout, char job, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int* ilo, lapack_int* ihi, float* scale );
lapack_int LAPACKE_zgebal( int matrix_layout, char job, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* ilo, lapack_int* ihi, double* scale );

lapack_int LAPACKE_sgebrd( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, float* d, float* e,
                           float* tauq, float* taup );
lapack_int LAPACKE_dgebrd( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, double* d, double* e,
                           double* tauq, double* taup );
lapack_int LAPACKE_cgebrd( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda, float* d,
                           float* e, lapack_complex_float* tauq,
                           lapack_complex_float* taup );
lapack_int LAPACKE_zgebrd( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda, double* d,
                           double* e, lapack_complex_double* tauq,
                           lapack_complex_double* taup );

lapack_int LAPACKE_sgecon( int matrix_layout, char norm, lapack_int n,
                           const float* a, lapack_int lda, float anorm,
                           float* rcond );
lapack_int LAPACKE_dgecon( int matrix_layout, char norm, lapack_int n,
                           const double* a, lapack_int lda, double anorm,
                           double* rcond );
lapack_int LAPACKE_cgecon( int matrix_layout, char norm, lapack_int n,
                           const lapack_complex_float* a, lapack_int lda,
                           float anorm, float* rcond );
lapack_int LAPACKE_zgecon( int matrix_layout, char norm, lapack_int n,
                           const lapack_complex_double* a, lapack_int lda,
                           double anorm, double* rcond );

lapack_int LAPACKE_sgeequ( int matrix_layout, lapack_int m, lapack_int n,
                           const float* a, lapack_int lda, float* r, float* c,
                           float* rowcnd, float* colcnd, float* amax );
lapack_int LAPACKE_dgeequ( int matrix_layout, lapack_int m, lapack_int n,
                           const double* a, lapack_int lda, double* r,
                           double* c, double* rowcnd, double* colcnd,
                           double* amax );
lapack_int LAPACKE_cgeequ( int matrix_layout, lapack_int m, lapack_int n,
                           const lapack_complex_float* a, lapack_int lda,
                           float* r, float* c, float* rowcnd, float* colcnd,
                           float* amax );
lapack_int LAPACKE_zgeequ( int matrix_layout, lapack_int m, lapack_int n,
                           const lapack_complex_double* a, lapack_int lda,
                           double* r, double* c, double* rowcnd, double* colcnd,
                           double* amax );

lapack_int LAPACKE_sgeequb( int matrix_layout, lapack_int m, lapack_int n,
                            const float* a, lapack_int lda, float* r, float* c,
                            float* rowcnd, float* colcnd, float* amax );
lapack_int LAPACKE_dgeequb( int matrix_layout, lapack_int m, lapack_int n,
                            const double* a, lapack_int lda, double* r,
                            double* c, double* rowcnd, double* colcnd,
                            double* amax );
lapack_int LAPACKE_cgeequb( int matrix_layout, lapack_int m, lapack_int n,
                            const lapack_complex_float* a, lapack_int lda,
                            float* r, float* c, float* rowcnd, float* colcnd,
                            float* amax );
lapack_int LAPACKE_zgeequb( int matrix_layout, lapack_int m, lapack_int n,
                            const lapack_complex_double* a, lapack_int lda,
                            double* r, double* c, double* rowcnd,
                            double* colcnd, double* amax );

lapack_int LAPACKE_sgees( int matrix_layout, char jobvs, char sort,
                          LAPACK_S_SELECT2 select, lapack_int n, float* a,
                          lapack_int lda, lapack_int* sdim, float* wr,
                          float* wi, float* vs, lapack_int ldvs );
lapack_int LAPACKE_dgees( int matrix_layout, char jobvs, char sort,
                          LAPACK_D_SELECT2 select, lapack_int n, double* a,
                          lapack_int lda, lapack_int* sdim, double* wr,
                          double* wi, double* vs, lapack_int ldvs );
lapack_int LAPACKE_cgees( int matrix_layout, char jobvs, char sort,
                          LAPACK_C_SELECT1 select, lapack_int n,
                          lapack_complex_float* a, lapack_int lda,
                          lapack_int* sdim, lapack_complex_float* w,
                          lapack_complex_float* vs, lapack_int ldvs );
lapack_int LAPACKE_zgees( int matrix_layout, char jobvs, char sort,
                          LAPACK_Z_SELECT1 select, lapack_int n,
                          lapack_complex_double* a, lapack_int lda,
                          lapack_int* sdim, lapack_complex_double* w,
                          lapack_complex_double* vs, lapack_int ldvs );

lapack_int LAPACKE_sgeesx( int matrix_layout, char jobvs, char sort,
                           LAPACK_S_SELECT2 select, char sense, lapack_int n,
                           float* a, lapack_int lda, lapack_int* sdim,
                           float* wr, float* wi, float* vs, lapack_int ldvs,
                           float* rconde, float* rcondv );
lapack_int LAPACKE_dgeesx( int matrix_layout, char jobvs, char sort,
                           LAPACK_D_SELECT2 select, char sense, lapack_int n,
                           double* a, lapack_int lda, lapack_int* sdim,
                           double* wr, double* wi, double* vs, lapack_int ldvs,
                           double* rconde, double* rcondv );
lapack_int LAPACKE_cgeesx( int matrix_layout, char jobvs, char sort,
                           LAPACK_C_SELECT1 select, char sense, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int* sdim, lapack_complex_float* w,
                           lapack_complex_float* vs, lapack_int ldvs,
                           float* rconde, float* rcondv );
lapack_int LAPACKE_zgeesx( int matrix_layout, char jobvs, char sort,
                           LAPACK_Z_SELECT1 select, char sense, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* sdim, lapack_complex_double* w,
                           lapack_complex_double* vs, lapack_int ldvs,
                           double* rconde, double* rcondv );

lapack_int LAPACKE_sgeev( int matrix_layout, char jobvl, char jobvr,
                          lapack_int n, float* a, lapack_int lda, float* wr,
                          float* wi, float* vl, lapack_int ldvl, float* vr,
                          lapack_int ldvr );
lapack_int LAPACKE_dgeev( int matrix_layout, char jobvl, char jobvr,
                          lapack_int n, double* a, lapack_int lda, double* wr,
                          double* wi, double* vl, lapack_int ldvl, double* vr,
                          lapack_int ldvr );
lapack_int LAPACKE_cgeev( int matrix_layout, char jobvl, char jobvr,
                          lapack_int n, lapack_complex_float* a, lapack_int lda,
                          lapack_complex_float* w, lapack_complex_float* vl,
                          lapack_int ldvl, lapack_complex_float* vr,
                          lapack_int ldvr );
lapack_int LAPACKE_zgeev( int matrix_layout, char jobvl, char jobvr,
                          lapack_int n, lapack_complex_double* a,
                          lapack_int lda, lapack_complex_double* w,
                          lapack_complex_double* vl, lapack_int ldvl,
                          lapack_complex_double* vr, lapack_int ldvr );

lapack_int LAPACKE_sgeevx( int matrix_layout, char balanc, char jobvl,
                           char jobvr, char sense, lapack_int n, float* a,
                           lapack_int lda, float* wr, float* wi, float* vl,
                           lapack_int ldvl, float* vr, lapack_int ldvr,
                           lapack_int* ilo, lapack_int* ihi, float* scale,
                           float* abnrm, float* rconde, float* rcondv );
lapack_int LAPACKE_dgeevx( int matrix_layout, char balanc, char jobvl,
                           char jobvr, char sense, lapack_int n, double* a,
                           lapack_int lda, double* wr, double* wi, double* vl,
                           lapack_int ldvl, double* vr, lapack_int ldvr,
                           lapack_int* ilo, lapack_int* ihi, double* scale,
                           double* abnrm, double* rconde, double* rcondv );
lapack_int LAPACKE_cgeevx( int matrix_layout, char balanc, char jobvl,
                           char jobvr, char sense, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* w, lapack_complex_float* vl,
                           lapack_int ldvl, lapack_complex_float* vr,
                           lapack_int ldvr, lapack_int* ilo, lapack_int* ihi,
                           float* scale, float* abnrm, float* rconde,
                           float* rcondv );
lapack_int LAPACKE_zgeevx( int matrix_layout, char balanc, char jobvl,
                           char jobvr, char sense, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* w, lapack_complex_double* vl,
                           lapack_int ldvl, lapack_complex_double* vr,
                           lapack_int ldvr, lapack_int* ilo, lapack_int* ihi,
                           double* scale, double* abnrm, double* rconde,
                           double* rcondv );

lapack_int LAPACKE_sgehrd( int matrix_layout, lapack_int n, lapack_int ilo,
                           lapack_int ihi, float* a, lapack_int lda,
                           float* tau );
lapack_int LAPACKE_dgehrd( int matrix_layout, lapack_int n, lapack_int ilo,
                           lapack_int ihi, double* a, lapack_int lda,
                           double* tau );
lapack_int LAPACKE_cgehrd( int matrix_layout, lapack_int n, lapack_int ilo,
                           lapack_int ihi, lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* tau );
lapack_int LAPACKE_zgehrd( int matrix_layout, lapack_int n, lapack_int ilo,
                           lapack_int ihi, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* tau );

lapack_int LAPACKE_sgejsv( int matrix_layout, char joba, char jobu, char jobv,
                           char jobr, char jobt, char jobp, lapack_int m,
                           lapack_int n, float* a, lapack_int lda, float* sva,
                           float* u, lapack_int ldu, float* v, lapack_int ldv,
                           float* stat, lapack_int* istat );
lapack_int LAPACKE_dgejsv( int matrix_layout, char joba, char jobu, char jobv,
                           char jobr, char jobt, char jobp, lapack_int m,
                           lapack_int n, double* a, lapack_int lda, double* sva,
                           double* u, lapack_int ldu, double* v, lapack_int ldv,
                           double* stat, lapack_int* istat );
lapack_int LAPACKE_cgejsv( int matrix_layout, char joba, char jobu, char jobv,
                           char jobr, char jobt, char jobp, lapack_int m,
                           lapack_int n, lapack_complex_float* a, lapack_int lda, float* sva,
                           lapack_complex_float* u, lapack_int ldu, lapack_complex_float* v, lapack_int ldv,
                           float* stat, lapack_int* istat );
lapack_int LAPACKE_zgejsv( int matrix_layout, char joba, char jobu, char jobv,
                           char jobr, char jobt, char jobp, lapack_int m,
                           lapack_int n, lapack_complex_double* a, lapack_int lda, double* sva,
                           lapack_complex_double* u, lapack_int ldu, lapack_complex_double* v, lapack_int ldv,
                           double* stat, lapack_int* istat );

lapack_int LAPACKE_sgelq2( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, float* tau );
lapack_int LAPACKE_dgelq2( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, double* tau );
lapack_int LAPACKE_cgelq2( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* tau );
lapack_int LAPACKE_zgelq2( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* tau );

lapack_int LAPACKE_sgelqf( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, float* tau );
lapack_int LAPACKE_dgelqf( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, double* tau );
lapack_int LAPACKE_cgelqf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* tau );
lapack_int LAPACKE_zgelqf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* tau );

lapack_int LAPACKE_sgels( int matrix_layout, char trans, lapack_int m,
                          lapack_int n, lapack_int nrhs, float* a,
                          lapack_int lda, float* b, lapack_int ldb );
lapack_int LAPACKE_dgels( int matrix_layout, char trans, lapack_int m,
                          lapack_int n, lapack_int nrhs, double* a,
                          lapack_int lda, double* b, lapack_int ldb );
lapack_int LAPACKE_cgels( int matrix_layout, char trans, lapack_int m,
                          lapack_int n, lapack_int nrhs,
                          lapack_complex_float* a, lapack_int lda,
                          lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zgels( int matrix_layout, char trans, lapack_int m,
                          lapack_int n, lapack_int nrhs,
                          lapack_complex_double* a, lapack_int lda,
                          lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_sgelsd( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, float* a, lapack_int lda, float* b,
                           lapack_int ldb, float* s, float rcond,
                           lapack_int* rank );
lapack_int LAPACKE_dgelsd( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, double* a, lapack_int lda,
                           double* b, lapack_int ldb, double* s, double rcond,
                           lapack_int* rank );
lapack_int LAPACKE_cgelsd( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* b,
                           lapack_int ldb, float* s, float rcond,
                           lapack_int* rank );
lapack_int LAPACKE_zgelsd( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* b,
                           lapack_int ldb, double* s, double rcond,
                           lapack_int* rank );

lapack_int LAPACKE_sgelss( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, float* a, lapack_int lda, float* b,
                           lapack_int ldb, float* s, float rcond,
                           lapack_int* rank );
lapack_int LAPACKE_dgelss( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, double* a, lapack_int lda,
                           double* b, lapack_int ldb, double* s, double rcond,
                           lapack_int* rank );
lapack_int LAPACKE_cgelss( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* b,
                           lapack_int ldb, float* s, float rcond,
                           lapack_int* rank );
lapack_int LAPACKE_zgelss( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* b,
                           lapack_int ldb, double* s, double rcond,
                           lapack_int* rank );

lapack_int LAPACKE_sgelsy( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, float* a, lapack_int lda, float* b,
                           lapack_int ldb, lapack_int* jpvt, float rcond,
                           lapack_int* rank );
lapack_int LAPACKE_dgelsy( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, double* a, lapack_int lda,
                           double* b, lapack_int ldb, lapack_int* jpvt,
                           double rcond, lapack_int* rank );
lapack_int LAPACKE_cgelsy( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* b,
                           lapack_int ldb, lapack_int* jpvt, float rcond,
                           lapack_int* rank );
lapack_int LAPACKE_zgelsy( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int nrhs, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* b,
                           lapack_int ldb, lapack_int* jpvt, double rcond,
                           lapack_int* rank );

lapack_int LAPACKE_sgeqlf( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, float* tau );
lapack_int LAPACKE_dgeqlf( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, double* tau );
lapack_int LAPACKE_cgeqlf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* tau );
lapack_int LAPACKE_zgeqlf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* tau );

lapack_int LAPACKE_sgeqp3( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, lapack_int* jpvt,
                           float* tau );
lapack_int LAPACKE_dgeqp3( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, lapack_int* jpvt,
                           double* tau );
lapack_int LAPACKE_cgeqp3( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int* jpvt, lapack_complex_float* tau );
lapack_int LAPACKE_zgeqp3( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* jpvt, lapack_complex_double* tau );

lapack_int LAPACKE_sgeqpf( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, lapack_int* jpvt,
                           float* tau );
lapack_int LAPACKE_dgeqpf( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, lapack_int* jpvt,
                           double* tau );
lapack_int LAPACKE_cgeqpf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int* jpvt, lapack_complex_float* tau );
lapack_int LAPACKE_zgeqpf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* jpvt, lapack_complex_double* tau );

lapack_int LAPACKE_sgeqr2( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, float* tau );
lapack_int LAPACKE_dgeqr2( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, double* tau );
lapack_int LAPACKE_cgeqr2( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* tau );
lapack_int LAPACKE_zgeqr2( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* tau );

lapack_int LAPACKE_sgeqrf( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, float* tau );
lapack_int LAPACKE_dgeqrf( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, double* tau );
lapack_int LAPACKE_cgeqrf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* tau );
lapack_int LAPACKE_zgeqrf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* tau );

lapack_int LAPACKE_sgeqrfp( int matrix_layout, lapack_int m, lapack_int n,
                            float* a, lapack_int lda, float* tau );
lapack_int LAPACKE_dgeqrfp( int matrix_layout, lapack_int m, lapack_int n,
                            double* a, lapack_int lda, double* tau );
lapack_int LAPACKE_cgeqrfp( int matrix_layout, lapack_int m, lapack_int n,
                            lapack_complex_float* a, lapack_int lda,
                            lapack_complex_float* tau );
lapack_int LAPACKE_zgeqrfp( int matrix_layout, lapack_int m, lapack_int n,
                            lapack_complex_double* a, lapack_int lda,
                            lapack_complex_double* tau );

lapack_int LAPACKE_sgerfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const float* a, lapack_int lda,
                           const float* af, lapack_int ldaf,
                           const lapack_int* ipiv, const float* b,
                           lapack_int ldb, float* x, lapack_int ldx,
                           float* ferr, float* berr );
lapack_int LAPACKE_dgerfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const double* a, lapack_int lda,
                           const double* af, lapack_int ldaf,
                           const lapack_int* ipiv, const double* b,
                           lapack_int ldb, double* x, lapack_int ldx,
                           double* ferr, double* berr );
lapack_int LAPACKE_cgerfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* a,
                           lapack_int lda, const lapack_complex_float* af,
                           lapack_int ldaf, const lapack_int* ipiv,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx, float* ferr,
                           float* berr );
lapack_int LAPACKE_zgerfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* a,
                           lapack_int lda, const lapack_complex_double* af,
                           lapack_int ldaf, const lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* ferr, double* berr );

lapack_int LAPACKE_sgerfsx( int matrix_layout, char trans, char equed,
                            lapack_int n, lapack_int nrhs, const float* a,
                            lapack_int lda, const float* af, lapack_int ldaf,
                            const lapack_int* ipiv, const float* r,
                            const float* c, const float* b, lapack_int ldb,
                            float* x, lapack_int ldx, float* rcond, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_dgerfsx( int matrix_layout, char trans, char equed,
                            lapack_int n, lapack_int nrhs, const double* a,
                            lapack_int lda, const double* af, lapack_int ldaf,
                            const lapack_int* ipiv, const double* r,
                            const double* c, const double* b, lapack_int ldb,
                            double* x, lapack_int ldx, double* rcond,
                            double* berr, lapack_int n_err_bnds,
                            double* err_bnds_norm, double* err_bnds_comp,
                            lapack_int nparams, double* params );
lapack_int LAPACKE_cgerfsx( int matrix_layout, char trans, char equed,
                            lapack_int n, lapack_int nrhs,
                            const lapack_complex_float* a, lapack_int lda,
                            const lapack_complex_float* af, lapack_int ldaf,
                            const lapack_int* ipiv, const float* r,
                            const float* c, const lapack_complex_float* b,
                            lapack_int ldb, lapack_complex_float* x,
                            lapack_int ldx, float* rcond, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_zgerfsx( int matrix_layout, char trans, char equed,
                            lapack_int n, lapack_int nrhs,
                            const lapack_complex_double* a, lapack_int lda,
                            const lapack_complex_double* af, lapack_int ldaf,
                            const lapack_int* ipiv, const double* r,
                            const double* c, const lapack_complex_double* b,
                            lapack_int ldb, lapack_complex_double* x,
                            lapack_int ldx, double* rcond, double* berr,
                            lapack_int n_err_bnds, double* err_bnds_norm,
                            double* err_bnds_comp, lapack_int nparams,
                            double* params );

lapack_int LAPACKE_sgerqf( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, float* tau );
lapack_int LAPACKE_dgerqf( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, double* tau );
lapack_int LAPACKE_cgerqf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* tau );
lapack_int LAPACKE_zgerqf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* tau );

lapack_int LAPACKE_sgesdd( int matrix_layout, char jobz, lapack_int m,
                           lapack_int n, float* a, lapack_int lda, float* s,
                           float* u, lapack_int ldu, float* vt,
                           lapack_int ldvt );
lapack_int LAPACKE_dgesdd( int matrix_layout, char jobz, lapack_int m,
                           lapack_int n, double* a, lapack_int lda, double* s,
                           double* u, lapack_int ldu, double* vt,
                           lapack_int ldvt );
lapack_int LAPACKE_cgesdd( int matrix_layout, char jobz, lapack_int m,
                           lapack_int n, lapack_complex_float* a,
                           lapack_int lda, float* s, lapack_complex_float* u,
                           lapack_int ldu, lapack_complex_float* vt,
                           lapack_int ldvt );
lapack_int LAPACKE_zgesdd( int matrix_layout, char jobz, lapack_int m,
                           lapack_int n, lapack_complex_double* a,
                           lapack_int lda, double* s, lapack_complex_double* u,
                           lapack_int ldu, lapack_complex_double* vt,
                           lapack_int ldvt );

lapack_int LAPACKE_sgesv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          float* a, lapack_int lda, lapack_int* ipiv, float* b,
                          lapack_int ldb );
lapack_int LAPACKE_dgesv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          double* a, lapack_int lda, lapack_int* ipiv,
                          double* b, lapack_int ldb );
lapack_int LAPACKE_cgesv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          lapack_complex_float* a, lapack_int lda,
                          lapack_int* ipiv, lapack_complex_float* b,
                          lapack_int ldb );
lapack_int LAPACKE_zgesv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          lapack_complex_double* a, lapack_int lda,
                          lapack_int* ipiv, lapack_complex_double* b,
                          lapack_int ldb );
lapack_int LAPACKE_dsgesv( int matrix_layout, lapack_int n, lapack_int nrhs,
                           double* a, lapack_int lda, lapack_int* ipiv,
                           double* b, lapack_int ldb, double* x, lapack_int ldx,
                           lapack_int* iter );
lapack_int LAPACKE_zcgesv( int matrix_layout, lapack_int n, lapack_int nrhs,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* ipiv, lapack_complex_double* b,
                           lapack_int ldb, lapack_complex_double* x,
                           lapack_int ldx, lapack_int* iter );

lapack_int LAPACKE_sgesvd( int matrix_layout, char jobu, char jobvt,
                           lapack_int m, lapack_int n, float* a, lapack_int lda,
                           float* s, float* u, lapack_int ldu, float* vt,
                           lapack_int ldvt, float* superb );
lapack_int LAPACKE_dgesvd( int matrix_layout, char jobu, char jobvt,
                           lapack_int m, lapack_int n, double* a,
                           lapack_int lda, double* s, double* u, lapack_int ldu,
                           double* vt, lapack_int ldvt, double* superb );
lapack_int LAPACKE_cgesvd( int matrix_layout, char jobu, char jobvt,
                           lapack_int m, lapack_int n, lapack_complex_float* a,
                           lapack_int lda, float* s, lapack_complex_float* u,
                           lapack_int ldu, lapack_complex_float* vt,
                           lapack_int ldvt, float* superb );
lapack_int LAPACKE_zgesvd( int matrix_layout, char jobu, char jobvt,
                           lapack_int m, lapack_int n, lapack_complex_double* a,
                           lapack_int lda, double* s, lapack_complex_double* u,
                           lapack_int ldu, lapack_complex_double* vt,
                           lapack_int ldvt, double* superb );

lapack_int LAPACKE_sgesvdx( int matrix_layout, char jobu, char jobvt, char range,
                           lapack_int m, lapack_int n, float* a,
                           lapack_int lda, float vl, float vu,
                           lapack_int il, lapack_int iu, lapack_int* ns,
                           float* s, float* u, lapack_int ldu,
                           float* vt, lapack_int ldvt,
                           lapack_int* superb );
lapack_int LAPACKE_dgesvdx( int matrix_layout, char jobu, char jobvt, char range,
                           lapack_int m, lapack_int n, double* a,
                           lapack_int lda, double vl, double vu,
                           lapack_int il, lapack_int iu, lapack_int* ns,
                           double* s, double* u, lapack_int ldu,
                           double* vt, lapack_int ldvt,
                           lapack_int* superb );
lapack_int LAPACKE_cgesvdx( int matrix_layout, char jobu, char jobvt, char range,
                           lapack_int m, lapack_int n, lapack_complex_float* a,
                           lapack_int lda, float vl, float vu,
                           lapack_int il, lapack_int iu, lapack_int* ns,
                           float* s, lapack_complex_float* u, lapack_int ldu,
                           lapack_complex_float* vt, lapack_int ldvt,
                           lapack_int* superb );
lapack_int LAPACKE_zgesvdx( int matrix_layout, char jobu, char jobvt, char range,
                           lapack_int m, lapack_int n, lapack_complex_double* a,
                           lapack_int lda, double vl, double vu,
                           lapack_int il, lapack_int iu, lapack_int* ns,
                           double* s, lapack_complex_double* u, lapack_int ldu,
                           lapack_complex_double* vt, lapack_int ldvt,
                           lapack_int* superb );

lapack_int LAPACKE_sgesvdq( int matrix_layout, char joba, char jobp, char jobr, char jobu, char jobv,
                           lapack_int m, lapack_int n, float* a, lapack_int lda,
                           float* s, float* u, lapack_int ldu, float* v,
                           lapack_int ldv, lapack_int* numrank );
lapack_int LAPACKE_dgesvdq( int matrix_layout, char joba, char jobp, char jobr, char jobu, char jobv,
                           lapack_int m, lapack_int n, double* a,
                           lapack_int lda, double* s, double* u, lapack_int ldu,
                           double* v, lapack_int ldv, lapack_int* numrank);
lapack_int LAPACKE_cgesvdq( int matrix_layout, char joba, char jobp, char jobr, char jobu, char jobv,
                           lapack_int m, lapack_int n, lapack_complex_float* a,
                           lapack_int lda, float* s, lapack_complex_float* u,
                           lapack_int ldu, lapack_complex_float* v,
                           lapack_int ldv, lapack_int* numrank );
lapack_int LAPACKE_zgesvdq( int matrix_layout, char joba, char jobp, char jobr, char jobu, char jobv,
                           lapack_int m, lapack_int n, lapack_complex_double* a,
                           lapack_int lda, double* s, lapack_complex_double* u,
                           lapack_int ldu, lapack_complex_double* v,
                           lapack_int ldv, lapack_int* numrank );
                           
lapack_int LAPACKE_sgesvj( int matrix_layout, char joba, char jobu, char jobv,
                           lapack_int m, lapack_int n, float* a, lapack_int lda,
                           float* sva, lapack_int mv, float* v, lapack_int ldv,
                           float* stat );
lapack_int LAPACKE_dgesvj( int matrix_layout, char joba, char jobu, char jobv,
                           lapack_int m, lapack_int n, double* a,
                           lapack_int lda, double* sva, lapack_int mv,
                           double* v, lapack_int ldv, double* stat );
lapack_int LAPACKE_cgesvj( int matrix_layout, char joba, char jobu, char jobv,
                           lapack_int m, lapack_int n, lapack_complex_float* a,
                           lapack_int lda, float* sva, lapack_int mv,
                           lapack_complex_float* v, lapack_int ldv, float* stat );
lapack_int LAPACKE_zgesvj( int matrix_layout, char joba, char jobu, char jobv,
                           lapack_int m, lapack_int n, lapack_complex_double* a,
                           lapack_int lda, double* sva, lapack_int mv,
                           lapack_complex_double* v, lapack_int ldv, double* stat );

lapack_int LAPACKE_sgesvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int nrhs, float* a,
                           lapack_int lda, float* af, lapack_int ldaf,
                           lapack_int* ipiv, char* equed, float* r, float* c,
                           float* b, lapack_int ldb, float* x, lapack_int ldx,
                           float* rcond, float* ferr, float* berr,
                           float* rpivot );
lapack_int LAPACKE_dgesvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int nrhs, double* a,
                           lapack_int lda, double* af, lapack_int ldaf,
                           lapack_int* ipiv, char* equed, double* r, double* c,
                           double* b, lapack_int ldb, double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr,
                           double* rpivot );
lapack_int LAPACKE_cgesvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int nrhs,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* af, lapack_int ldaf,
                           lapack_int* ipiv, char* equed, float* r, float* c,
                           lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx,
                           float* rcond, float* ferr, float* berr,
                           float* rpivot );
lapack_int LAPACKE_zgesvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int nrhs,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* af, lapack_int ldaf,
                           lapack_int* ipiv, char* equed, double* r, double* c,
                           lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr,
                           double* rpivot );

lapack_int LAPACKE_sgesvxx( int matrix_layout, char fact, char trans,
                            lapack_int n, lapack_int nrhs, float* a,
                            lapack_int lda, float* af, lapack_int ldaf,
                            lapack_int* ipiv, char* equed, float* r, float* c,
                            float* b, lapack_int ldb, float* x, lapack_int ldx,
                            float* rcond, float* rpvgrw, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_dgesvxx( int matrix_layout, char fact, char trans,
                            lapack_int n, lapack_int nrhs, double* a,
                            lapack_int lda, double* af, lapack_int ldaf,
                            lapack_int* ipiv, char* equed, double* r, double* c,
                            double* b, lapack_int ldb, double* x,
                            lapack_int ldx, double* rcond, double* rpvgrw,
                            double* berr, lapack_int n_err_bnds,
                            double* err_bnds_norm, double* err_bnds_comp,
                            lapack_int nparams, double* params );
lapack_int LAPACKE_cgesvxx( int matrix_layout, char fact, char trans,
                            lapack_int n, lapack_int nrhs,
                            lapack_complex_float* a, lapack_int lda,
                            lapack_complex_float* af, lapack_int ldaf,
                            lapack_int* ipiv, char* equed, float* r, float* c,
                            lapack_complex_float* b, lapack_int ldb,
                            lapack_complex_float* x, lapack_int ldx,
                            float* rcond, float* rpvgrw, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_zgesvxx( int matrix_layout, char fact, char trans,
                            lapack_int n, lapack_int nrhs,
                            lapack_complex_double* a, lapack_int lda,
                            lapack_complex_double* af, lapack_int ldaf,
                            lapack_int* ipiv, char* equed, double* r, double* c,
                            lapack_complex_double* b, lapack_int ldb,
                            lapack_complex_double* x, lapack_int ldx,
                            double* rcond, double* rpvgrw, double* berr,
                            lapack_int n_err_bnds, double* err_bnds_norm,
                            double* err_bnds_comp, lapack_int nparams,
                            double* params );

lapack_int LAPACKE_sgetf2( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, lapack_int* ipiv );
lapack_int LAPACKE_dgetf2( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, lapack_int* ipiv );
lapack_int LAPACKE_cgetf2( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int* ipiv );
lapack_int LAPACKE_zgetf2( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* ipiv );

lapack_int LAPACKE_sgetrf( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, lapack_int* ipiv );
lapack_int LAPACKE_dgetrf( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, lapack_int* ipiv );
lapack_int LAPACKE_cgetrf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int* ipiv );
lapack_int LAPACKE_zgetrf( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* ipiv );

lapack_int LAPACKE_sgetrf2( int matrix_layout, lapack_int m, lapack_int n,
                           float* a, lapack_int lda, lapack_int* ipiv );
lapack_int LAPACKE_dgetrf2( int matrix_layout, lapack_int m, lapack_int n,
                           double* a, lapack_int lda, lapack_int* ipiv );
lapack_int LAPACKE_cgetrf2( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int* ipiv );
lapack_int LAPACKE_zgetrf2( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* ipiv );

lapack_int LAPACKE_sgetri( int matrix_layout, lapack_int n, float* a,
                           lapack_int lda, const lapack_int* ipiv );
lapack_int LAPACKE_dgetri( int matrix_layout, lapack_int n, double* a,
                           lapack_int lda, const lapack_int* ipiv );
lapack_int LAPACKE_cgetri( int matrix_layout, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           const lapack_int* ipiv );
lapack_int LAPACKE_zgetri( int matrix_layout, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           const lapack_int* ipiv );

lapack_int LAPACKE_sgetrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const float* a, lapack_int lda,
                           const lapack_int* ipiv, float* b, lapack_int ldb );
lapack_int LAPACKE_dgetrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const double* a, lapack_int lda,
                           const lapack_int* ipiv, double* b, lapack_int ldb );
lapack_int LAPACKE_cgetrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* a,
                           lapack_int lda, const lapack_int* ipiv,
                           lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zgetrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* a,
                           lapack_int lda, const lapack_int* ipiv,
                           lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_sggbak( int matrix_layout, char job, char side, lapack_int n,
                           lapack_int ilo, lapack_int ihi, const float* lscale,
                           const float* rscale, lapack_int m, float* v,
                           lapack_int ldv );
lapack_int LAPACKE_dggbak( int matrix_layout, char job, char side, lapack_int n,
                           lapack_int ilo, lapack_int ihi, const double* lscale,
                           const double* rscale, lapack_int m, double* v,
                           lapack_int ldv );
lapack_int LAPACKE_cggbak( int matrix_layout, char job, char side, lapack_int n,
                           lapack_int ilo, lapack_int ihi, const float* lscale,
                           const float* rscale, lapack_int m,
                           lapack_complex_float* v, lapack_int ldv );
lapack_int LAPACKE_zggbak( int matrix_layout, char job, char side, lapack_int n,
                           lapack_int ilo, lapack_int ihi, const double* lscale,
                           const double* rscale, lapack_int m,
                           lapack_complex_double* v, lapack_int ldv );

lapack_int LAPACKE_sggbal( int matrix_layout, char job, lapack_int n, float* a,
                           lapack_int lda, float* b, lapack_int ldb,
                           lapack_int* ilo, lapack_int* ihi, float* lscale,
                           float* rscale );
lapack_int LAPACKE_dggbal( int matrix_layout, char job, lapack_int n, double* a,
                           lapack_int lda, double* b, lapack_int ldb,
                           lapack_int* ilo, lapack_int* ihi, double* lscale,
                           double* rscale );
lapack_int LAPACKE_cggbal( int matrix_layout, char job, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* b, lapack_int ldb,
                           lapack_int* ilo, lapack_int* ihi, float* lscale,
                           float* rscale );
lapack_int LAPACKE_zggbal( int matrix_layout, char job, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* b, lapack_int ldb,
                           lapack_int* ilo, lapack_int* ihi, double* lscale,
                           double* rscale );

lapack_int LAPACKE_sgges( int matrix_layout, char jobvsl, char jobvsr, char sort,
                          LAPACK_S_SELECT3 selctg, lapack_int n, float* a,
                          lapack_int lda, float* b, lapack_int ldb,
                          lapack_int* sdim, float* alphar, float* alphai,
                          float* beta, float* vsl, lapack_int ldvsl, float* vsr,
                          lapack_int ldvsr );
lapack_int LAPACKE_dgges( int matrix_layout, char jobvsl, char jobvsr, char sort,
                          LAPACK_D_SELECT3 selctg, lapack_int n, double* a,
                          lapack_int lda, double* b, lapack_int ldb,
                          lapack_int* sdim, double* alphar, double* alphai,
                          double* beta, double* vsl, lapack_int ldvsl,
                          double* vsr, lapack_int ldvsr );
lapack_int LAPACKE_cgges( int matrix_layout, char jobvsl, char jobvsr, char sort,
                          LAPACK_C_SELECT2 selctg, lapack_int n,
                          lapack_complex_float* a, lapack_int lda,
                          lapack_complex_float* b, lapack_int ldb,
                          lapack_int* sdim, lapack_complex_float* alpha,
                          lapack_complex_float* beta, lapack_complex_float* vsl,
                          lapack_int ldvsl, lapack_complex_float* vsr,
                          lapack_int ldvsr );
lapack_int LAPACKE_zgges( int matrix_layout, char jobvsl, char jobvsr, char sort,
                          LAPACK_Z_SELECT2 selctg, lapack_int n,
                          lapack_complex_double* a, lapack_int lda,
                          lapack_complex_double* b, lapack_int ldb,
                          lapack_int* sdim, lapack_complex_double* alpha,
                          lapack_complex_double* beta,
                          lapack_complex_double* vsl, lapack_int ldvsl,
                          lapack_complex_double* vsr, lapack_int ldvsr );

lapack_int LAPACKE_sgges3( int matrix_layout, char jobvsl, char jobvsr,
                           char sort, LAPACK_S_SELECT3 selctg, lapack_int n,
                           float* a, lapack_int lda, float* b, lapack_int ldb,
                           lapack_int* sdim, float* alphar, float* alphai,
                           float* beta, float* vsl, lapack_int ldvsl,
                           float* vsr, lapack_int ldvsr );
lapack_int LAPACKE_dgges3( int matrix_layout, char jobvsl, char jobvsr,
                           char sort, LAPACK_D_SELECT3 selctg, lapack_int n,
                           double* a, lapack_int lda, double* b, lapack_int ldb,
                           lapack_int* sdim, double* alphar, double* alphai,
                           double* beta, double* vsl, lapack_int ldvsl,
                           double* vsr, lapack_int ldvsr );
lapack_int LAPACKE_cgges3( int matrix_layout, char jobvsl, char jobvsr,
                           char sort, LAPACK_C_SELECT2 selctg, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* b, lapack_int ldb,
                           lapack_int* sdim, lapack_complex_float* alpha,
                           lapack_complex_float* beta,
                           lapack_complex_float* vsl, lapack_int ldvsl,
                           lapack_complex_float* vsr, lapack_int ldvsr );
lapack_int LAPACKE_zgges3( int matrix_layout, char jobvsl, char jobvsr,
                           char sort, LAPACK_Z_SELECT2 selctg, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* b, lapack_int ldb,
                           lapack_int* sdim, lapack_complex_double* alpha,
                           lapack_complex_double* beta,
                           lapack_complex_double* vsl, lapack_int ldvsl,
                           lapack_complex_double* vsr, lapack_int ldvsr );

lapack_int LAPACKE_sggesx( int matrix_layout, char jobvsl, char jobvsr,
                           char sort, LAPACK_S_SELECT3 selctg, char sense,
                           lapack_int n, float* a, lapack_int lda, float* b,
                           lapack_int ldb, lapack_int* sdim, float* alphar,
                           float* alphai, float* beta, float* vsl,
                           lapack_int ldvsl, float* vsr, lapack_int ldvsr,
                           float* rconde, float* rcondv );
lapack_int LAPACKE_dggesx( int matrix_layout, char jobvsl, char jobvsr,
                           char sort, LAPACK_D_SELECT3 selctg, char sense,
                           lapack_int n, double* a, lapack_int lda, double* b,
                           lapack_int ldb, lapack_int* sdim, double* alphar,
                           double* alphai, double* beta, double* vsl,
                           lapack_int ldvsl, double* vsr, lapack_int ldvsr,
                           double* rconde, double* rcondv );
lapack_int LAPACKE_cggesx( int matrix_layout, char jobvsl, char jobvsr,
                           char sort, LAPACK_C_SELECT2 selctg, char sense,
                           lapack_int n, lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* b,
                           lapack_int ldb, lapack_int* sdim,
                           lapack_complex_float* alpha,
                           lapack_complex_float* beta,
                           lapack_complex_float* vsl, lapack_int ldvsl,
                           lapack_complex_float* vsr, lapack_int ldvsr,
                           float* rconde, float* rcondv );
lapack_int LAPACKE_zggesx( int matrix_layout, char jobvsl, char jobvsr,
                           char sort, LAPACK_Z_SELECT2 selctg, char sense,
                           lapack_int n, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* b,
                           lapack_int ldb, lapack_int* sdim,
                           lapack_complex_double* alpha,
                           lapack_complex_double* beta,
                           lapack_complex_double* vsl, lapack_int ldvsl,
                           lapack_complex_double* vsr, lapack_int ldvsr,
                           double* rconde, double* rcondv );

lapack_int LAPACKE_sggev( int matrix_layout, char jobvl, char jobvr,
                          lapack_int n, float* a, lapack_int lda, float* b,
                          lapack_int ldb, float* alphar, float* alphai,
                          float* beta, float* vl, lapack_int ldvl, float* vr,
                          lapack_int ldvr );
lapack_int LAPACKE_dggev( int matrix_layout, char jobvl, char jobvr,
                          lapack_int n, double* a, lapack_int lda, double* b,
                          lapack_int ldb, double* alphar, double* alphai,
                          double* beta, double* vl, lapack_int ldvl, double* vr,
                          lapack_int ldvr );
lapack_int LAPACKE_cggev( int matrix_layout, char jobvl, char jobvr,
                          lapack_int n, lapack_complex_float* a, lapack_int lda,
                          lapack_complex_float* b, lapack_int ldb,
                          lapack_complex_float* alpha,
                          lapack_complex_float* beta, lapack_complex_float* vl,
                          lapack_int ldvl, lapack_complex_float* vr,
                          lapack_int ldvr );
lapack_int LAPACKE_zggev( int matrix_layout, char jobvl, char jobvr,
                          lapack_int n, lapack_complex_double* a,
                          lapack_int lda, lapack_complex_double* b,
                          lapack_int ldb, lapack_complex_double* alpha,
                          lapack_complex_double* beta,
                          lapack_complex_double* vl, lapack_int ldvl,
                          lapack_complex_double* vr, lapack_int ldvr );

lapack_int LAPACKE_sggev3( int matrix_layout, char jobvl, char jobvr,
                           lapack_int n, float* a, lapack_int lda,
                           float* b, lapack_int ldb,
                           float* alphar, float* alphai, float* beta,
                           float* vl, lapack_int ldvl,
                           float* vr, lapack_int ldvr );
lapack_int LAPACKE_dggev3( int matrix_layout, char jobvl, char jobvr,
                           lapack_int n, double* a, lapack_int lda,
                           double* b, lapack_int ldb,
                           double* alphar, double* alphai, double* beta,
                           double* vl, lapack_int ldvl,
                           double* vr, lapack_int ldvr );
lapack_int LAPACKE_cggev3( int matrix_layout, char jobvl, char jobvr,
                           lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* alpha,
                           lapack_complex_float* beta,
                           lapack_complex_float* vl, lapack_int ldvl,
                           lapack_complex_float* vr, lapack_int ldvr );
lapack_int LAPACKE_zggev3( int matrix_layout, char jobvl, char jobvr,
                           lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* alpha,
                           lapack_complex_double* beta,
                           lapack_complex_double* vl, lapack_int ldvl,
                           lapack_complex_double* vr, lapack_int ldvr );

lapack_int LAPACKE_sggevx( int matrix_layout, char balanc, char jobvl,
                           char jobvr, char sense, lapack_int n, float* a,
                           lapack_int lda, float* b, lapack_int ldb,
                           float* alphar, float* alphai, float* beta, float* vl,
                           lapack_int ldvl, float* vr, lapack_int ldvr,
                           lapack_int* ilo, lapack_int* ihi, float* lscale,
                           float* rscale, float* abnrm, float* bbnrm,
                           float* rconde, float* rcondv );
lapack_int LAPACKE_dggevx( int matrix_layout, char balanc, char jobvl,
                           char jobvr, char sense, lapack_int n, double* a,
                           lapack_int lda, double* b, lapack_int ldb,
                           double* alphar, double* alphai, double* beta,
                           double* vl, lapack_int ldvl, double* vr,
                           lapack_int ldvr, lapack_int* ilo, lapack_int* ihi,
                           double* lscale, double* rscale, double* abnrm,
                           double* bbnrm, double* rconde, double* rcondv );
lapack_int LAPACKE_cggevx( int matrix_layout, char balanc, char jobvl,
                           char jobvr, char sense, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* alpha,
                           lapack_complex_float* beta, lapack_complex_float* vl,
                           lapack_int ldvl, lapack_complex_float* vr,
                           lapack_int ldvr, lapack_int* ilo, lapack_int* ihi,
                           float* lscale, float* rscale, float* abnrm,
                           float* bbnrm, float* rconde, float* rcondv );
lapack_int LAPACKE_zggevx( int matrix_layout, char balanc, char jobvl,
                           char jobvr, char sense, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* alpha,
                           lapack_complex_double* beta,
                           lapack_complex_double* vl, lapack_int ldvl,
                           lapack_complex_double* vr, lapack_int ldvr,
                           lapack_int* ilo, lapack_int* ihi, double* lscale,
                           double* rscale, double* abnrm, double* bbnrm,
                           double* rconde, double* rcondv );

lapack_int LAPACKE_sggglm( int matrix_layout, lapack_int n, lapack_int m,
                           lapack_int p, float* a, lapack_int lda, float* b,
                           lapack_int ldb, float* d, float* x, float* y );
lapack_int LAPACKE_dggglm( int matrix_layout, lapack_int n, lapack_int m,
                           lapack_int p, double* a, lapack_int lda, double* b,
                           lapack_int ldb, double* d, double* x, double* y );
lapack_int LAPACKE_cggglm( int matrix_layout, lapack_int n, lapack_int m,
                           lapack_int p, lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* b,
                           lapack_int ldb, lapack_complex_float* d,
                           lapack_complex_float* x, lapack_complex_float* y );
lapack_int LAPACKE_zggglm( int matrix_layout, lapack_int n, lapack_int m,
                           lapack_int p, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* b,
                           lapack_int ldb, lapack_complex_double* d,
                           lapack_complex_double* x, lapack_complex_double* y );

lapack_int LAPACKE_sgghrd( int matrix_layout, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           float* a, lapack_int lda, float* b, lapack_int ldb,
                           float* q, lapack_int ldq, float* z, lapack_int ldz );
lapack_int LAPACKE_dgghrd( int matrix_layout, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           double* a, lapack_int lda, double* b, lapack_int ldb,
                           double* q, lapack_int ldq, double* z,
                           lapack_int ldz );
lapack_int LAPACKE_cgghrd( int matrix_layout, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* q, lapack_int ldq,
                           lapack_complex_float* z, lapack_int ldz );
lapack_int LAPACKE_zgghrd( int matrix_layout, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* q, lapack_int ldq,
                           lapack_complex_double* z, lapack_int ldz );

lapack_int LAPACKE_sgghd3( int matrix_layout, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           float* a, lapack_int lda, float* b, lapack_int ldb,
                           float* q, lapack_int ldq, float* z, lapack_int ldz );
lapack_int LAPACKE_dgghd3( int matrix_layout, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           double* a, lapack_int lda, double* b, lapack_int ldb,
                           double* q, lapack_int ldq, double* z,
                           lapack_int ldz );
lapack_int LAPACKE_cgghd3( int matrix_layout, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* q, lapack_int ldq,
                           lapack_complex_float* z, lapack_int ldz );
lapack_int LAPACKE_zgghd3( int matrix_layout, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* q, lapack_int ldq,
                           lapack_complex_double* z, lapack_int ldz );

lapack_int LAPACKE_sgglse( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int p, float* a, lapack_int lda, float* b,
                           lapack_int ldb, float* c, float* d, float* x );
lapack_int LAPACKE_dgglse( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int p, double* a, lapack_int lda, double* b,
                           lapack_int ldb, double* c, double* d, double* x );
lapack_int LAPACKE_cgglse( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int p, lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* b,
                           lapack_int ldb, lapack_complex_float* c,
                           lapack_complex_float* d, lapack_complex_float* x );
lapack_int LAPACKE_zgglse( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int p, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* b,
                           lapack_int ldb, lapack_complex_double* c,
                           lapack_complex_double* d, lapack_complex_double* x );

lapack_int LAPACKE_sggqrf( int matrix_layout, lapack_int n, lapack_int m,
                           lapack_int p, float* a, lapack_int lda, float* taua,
                           float* b, lapack_int ldb, float* taub );
lapack_int LAPACKE_dggqrf( int matrix_layout, lapack_int n, lapack_int m,
                           lapack_int p, double* a, lapack_int lda,
                           double* taua, double* b, lapack_int ldb,
                           double* taub );
lapack_int LAPACKE_cggqrf( int matrix_layout, lapack_int n, lapack_int m,
                           lapack_int p, lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* taua,
                           lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* taub );
lapack_int LAPACKE_zggqrf( int matrix_layout, lapack_int n, lapack_int m,
                           lapack_int p, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* taua,
                           lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* taub );

lapack_int LAPACKE_sggrqf( int matrix_layout, lapack_int m, lapack_int p,
                           lapack_int n, float* a, lapack_int lda, float* taua,
                           float* b, lapack_int ldb, float* taub );
lapack_int LAPACKE_dggrqf( int matrix_layout, lapack_int m, lapack_int p,
                           lapack_int n, double* a, lapack_int lda,
                           double* taua, double* b, lapack_int ldb,
                           double* taub );
lapack_int LAPACKE_cggrqf( int matrix_layout, lapack_int m, lapack_int p,
                           lapack_int n, lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* taua,
                           lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* taub );
lapack_int LAPACKE_zggrqf( int matrix_layout, lapack_int m, lapack_int p,
                           lapack_int n, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* taua,
                           lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* taub );

lapack_int LAPACKE_sggsvd( int matrix_layout, char jobu, char jobv, char jobq,
                           lapack_int m, lapack_int n, lapack_int p,
                           lapack_int* k, lapack_int* l, float* a,
                           lapack_int lda, float* b, lapack_int ldb,
                           float* alpha, float* beta, float* u, lapack_int ldu,
                           float* v, lapack_int ldv, float* q, lapack_int ldq,
                           lapack_int* iwork );
lapack_int LAPACKE_dggsvd( int matrix_layout, char jobu, char jobv, char jobq,
                           lapack_int m, lapack_int n, lapack_int p,
                           lapack_int* k, lapack_int* l, double* a,
                           lapack_int lda, double* b, lapack_int ldb,
                           double* alpha, double* beta, double* u,
                           lapack_int ldu, double* v, lapack_int ldv, double* q,
                           lapack_int ldq, lapack_int* iwork );
lapack_int LAPACKE_cggsvd( int matrix_layout, char jobu, char jobv, char jobq,
                           lapack_int m, lapack_int n, lapack_int p,
                           lapack_int* k, lapack_int* l,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* b, lapack_int ldb,
                           float* alpha, float* beta, lapack_complex_float* u,
                           lapack_int ldu, lapack_complex_float* v,
                           lapack_int ldv, lapack_complex_float* q,
                           lapack_int ldq, lapack_int* iwork );
lapack_int LAPACKE_zggsvd( int matrix_layout, char jobu, char jobv, char jobq,
                           lapack_int m, lapack_int n, lapack_int p,
                           lapack_int* k, lapack_int* l,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* b, lapack_int ldb,
                           double* alpha, double* beta,
                           lapack_complex_double* u, lapack_int ldu,
                           lapack_complex_double* v, lapack_int ldv,
                           lapack_complex_double* q, lapack_int ldq,
                           lapack_int* iwork );

lapack_int LAPACKE_sggsvd3( int matrix_layout, char jobu, char jobv, char jobq,
                            lapack_int m, lapack_int n, lapack_int p,
                            lapack_int* k, lapack_int* l, float* a,
                            lapack_int lda, float* b, lapack_int ldb,
                            float* alpha, float* beta, float* u, lapack_int ldu,
                            float* v, lapack_int ldv, float* q, lapack_int ldq,
                            lapack_int* iwork );
lapack_int LAPACKE_dggsvd3( int matrix_layout, char jobu, char jobv, char jobq,
                            lapack_int m, lapack_int n, lapack_int p,
                            lapack_int* k, lapack_int* l, double* a,
                            lapack_int lda, double* b, lapack_int ldb,
                            double* alpha, double* beta, double* u,
                            lapack_int ldu, double* v, lapack_int ldv, double* q,
                            lapack_int ldq, lapack_int* iwork );
lapack_int LAPACKE_cggsvd3( int matrix_layout, char jobu, char jobv, char jobq,
                            lapack_int m, lapack_int n, lapack_int p,
                            lapack_int* k, lapack_int* l,
                            lapack_complex_float* a, lapack_int lda,
                            lapack_complex_float* b, lapack_int ldb,
                            float* alpha, float* beta, lapack_complex_float* u,
                            lapack_int ldu, lapack_complex_float* v,
                            lapack_int ldv, lapack_complex_float* q,
                            lapack_int ldq, lapack_int* iwork );
lapack_int LAPACKE_zggsvd3( int matrix_layout, char jobu, char jobv, char jobq,
                            lapack_int m, lapack_int n, lapack_int p,
                            lapack_int* k, lapack_int* l,
                            lapack_complex_double* a, lapack_int lda,
                            lapack_complex_double* b, lapack_int ldb,
                            double* alpha, double* beta,
                            lapack_complex_double* u, lapack_int ldu,
                            lapack_complex_double* v, lapack_int ldv,
                            lapack_complex_double* q, lapack_int ldq,
                            lapack_int* iwork );

lapack_int LAPACKE_sggsvp( int matrix_layout, char jobu, char jobv, char jobq,
                           lapack_int m, lapack_int p, lapack_int n, float* a,
                           lapack_int lda, float* b, lapack_int ldb, float tola,
                           float tolb, lapack_int* k, lapack_int* l, float* u,
                           lapack_int ldu, float* v, lapack_int ldv, float* q,
                           lapack_int ldq );
lapack_int LAPACKE_dggsvp( int matrix_layout, char jobu, char jobv, char jobq,
                           lapack_int m, lapack_int p, lapack_int n, double* a,
                           lapack_int lda, double* b, lapack_int ldb,
                           double tola, double tolb, lapack_int* k,
                           lapack_int* l, double* u, lapack_int ldu, double* v,
                           lapack_int ldv, double* q, lapack_int ldq );
lapack_int LAPACKE_cggsvp( int matrix_layout, char jobu, char jobv, char jobq,
                           lapack_int m, lapack_int p, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* b, lapack_int ldb, float tola,
                           float tolb, lapack_int* k, lapack_int* l,
                           lapack_complex_float* u, lapack_int ldu,
                           lapack_complex_float* v, lapack_int ldv,
                           lapack_complex_float* q, lapack_int ldq );
lapack_int LAPACKE_zggsvp( int matrix_layout, char jobu, char jobv, char jobq,
                           lapack_int m, lapack_int p, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* b, lapack_int ldb,
                           double tola, double tolb, lapack_int* k,
                           lapack_int* l, lapack_complex_double* u,
                           lapack_int ldu, lapack_complex_double* v,
                           lapack_int ldv, lapack_complex_double* q,
                           lapack_int ldq );

lapack_int LAPACKE_sggsvp3( int matrix_layout, char jobu, char jobv, char jobq,
                            lapack_int m, lapack_int p, lapack_int n, float* a,
                            lapack_int lda, float* b, lapack_int ldb, float tola,
                            float tolb, lapack_int* k, lapack_int* l, float* u,
                            lapack_int ldu, float* v, lapack_int ldv, float* q,
                            lapack_int ldq );
lapack_int LAPACKE_dggsvp3( int matrix_layout, char jobu, char jobv, char jobq,
                            lapack_int m, lapack_int p, lapack_int n, double* a,
                            lapack_int lda, double* b, lapack_int ldb,
                            double tola, double tolb, lapack_int* k,
                            lapack_int* l, double* u, lapack_int ldu, double* v,
                            lapack_int ldv, double* q, lapack_int ldq );
lapack_int LAPACKE_cggsvp3( int matrix_layout, char jobu, char jobv, char jobq,
                            lapack_int m, lapack_int p, lapack_int n,
                            lapack_complex_float* a, lapack_int lda,
                            lapack_complex_float* b, lapack_int ldb, float tola,
                            float tolb, lapack_int* k, lapack_int* l,
                            lapack_complex_float* u, lapack_int ldu,
                            lapack_complex_float* v, lapack_int ldv,
                            lapack_complex_float* q, lapack_int ldq );
lapack_int LAPACKE_zggsvp3( int matrix_layout, char jobu, char jobv, char jobq,
                            lapack_int m, lapack_int p, lapack_int n,
                            lapack_complex_double* a, lapack_int lda,
                            lapack_complex_double* b, lapack_int ldb,
                            double tola, double tolb, lapack_int* k,
                            lapack_int* l, lapack_complex_double* u,
                            lapack_int ldu, lapack_complex_double* v,
                            lapack_int ldv, lapack_complex_double* q,
                            lapack_int ldq );

lapack_int LAPACKE_sgtcon( char norm, lapack_int n, const float* dl,
                           const float* d, const float* du, const float* du2,
                           const lapack_int* ipiv, float anorm, float* rcond );
lapack_int LAPACKE_dgtcon( char norm, lapack_int n, const double* dl,
                           const double* d, const double* du, const double* du2,
                           const lapack_int* ipiv, double anorm,
                           double* rcond );
lapack_int LAPACKE_cgtcon( char norm, lapack_int n,
                           const lapack_complex_float* dl,
                           const lapack_complex_float* d,
                           const lapack_complex_float* du,
                           const lapack_complex_float* du2,
                           const lapack_int* ipiv, float anorm, float* rcond );
lapack_int LAPACKE_zgtcon( char norm, lapack_int n,
                           const lapack_complex_double* dl,
                           const lapack_complex_double* d,
                           const lapack_complex_double* du,
                           const lapack_complex_double* du2,
                           const lapack_int* ipiv, double anorm,
                           double* rcond );

lapack_int LAPACKE_sgtrfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const float* dl, const float* d,
                           const float* du, const float* dlf, const float* df,
                           const float* duf, const float* du2,
                           const lapack_int* ipiv, const float* b,
                           lapack_int ldb, float* x, lapack_int ldx,
                           float* ferr, float* berr );
lapack_int LAPACKE_dgtrfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const double* dl, const double* d,
                           const double* du, const double* dlf,
                           const double* df, const double* duf,
                           const double* du2, const lapack_int* ipiv,
                           const double* b, lapack_int ldb, double* x,
                           lapack_int ldx, double* ferr, double* berr );
lapack_int LAPACKE_cgtrfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* dl,
                           const lapack_complex_float* d,
                           const lapack_complex_float* du,
                           const lapack_complex_float* dlf,
                           const lapack_complex_float* df,
                           const lapack_complex_float* duf,
                           const lapack_complex_float* du2,
                           const lapack_int* ipiv,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx, float* ferr,
                           float* berr );
lapack_int LAPACKE_zgtrfs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* dl,
                           const lapack_complex_double* d,
                           const lapack_complex_double* du,
                           const lapack_complex_double* dlf,
                           const lapack_complex_double* df,
                           const lapack_complex_double* duf,
                           const lapack_complex_double* du2,
                           const lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* ferr, double* berr );

lapack_int LAPACKE_sgtsv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          float* dl, float* d, float* du, float* b,
                          lapack_int ldb );
lapack_int LAPACKE_dgtsv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          double* dl, double* d, double* du, double* b,
                          lapack_int ldb );
lapack_int LAPACKE_cgtsv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          lapack_complex_float* dl, lapack_complex_float* d,
                          lapack_complex_float* du, lapack_complex_float* b,
                          lapack_int ldb );
lapack_int LAPACKE_zgtsv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          lapack_complex_double* dl, lapack_complex_double* d,
                          lapack_complex_double* du, lapack_complex_double* b,
                          lapack_int ldb );

lapack_int LAPACKE_sgtsvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int nrhs, const float* dl,
                           const float* d, const float* du, float* dlf,
                           float* df, float* duf, float* du2, lapack_int* ipiv,
                           const float* b, lapack_int ldb, float* x,
                           lapack_int ldx, float* rcond, float* ferr,
                           float* berr );
lapack_int LAPACKE_dgtsvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int nrhs, const double* dl,
                           const double* d, const double* du, double* dlf,
                           double* df, double* duf, double* du2,
                           lapack_int* ipiv, const double* b, lapack_int ldb,
                           double* x, lapack_int ldx, double* rcond,
                           double* ferr, double* berr );
lapack_int LAPACKE_cgtsvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int nrhs,
                           const lapack_complex_float* dl,
                           const lapack_complex_float* d,
                           const lapack_complex_float* du,
                           lapack_complex_float* dlf, lapack_complex_float* df,
                           lapack_complex_float* duf, lapack_complex_float* du2,
                           lapack_int* ipiv, const lapack_complex_float* b,
                           lapack_int ldb, lapack_complex_float* x,
                           lapack_int ldx, float* rcond, float* ferr,
                           float* berr );
lapack_int LAPACKE_zgtsvx( int matrix_layout, char fact, char trans,
                           lapack_int n, lapack_int nrhs,
                           const lapack_complex_double* dl,
                           const lapack_complex_double* d,
                           const lapack_complex_double* du,
                           lapack_complex_double* dlf,
                           lapack_complex_double* df,
                           lapack_complex_double* duf,
                           lapack_complex_double* du2, lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr );

lapack_int LAPACKE_sgttrf( lapack_int n, float* dl, float* d, float* du,
                           float* du2, lapack_int* ipiv );
lapack_int LAPACKE_dgttrf( lapack_int n, double* dl, double* d, double* du,
                           double* du2, lapack_int* ipiv );
lapack_int LAPACKE_cgttrf( lapack_int n, lapack_complex_float* dl,
                           lapack_complex_float* d, lapack_complex_float* du,
                           lapack_complex_float* du2, lapack_int* ipiv );
lapack_int LAPACKE_zgttrf( lapack_int n, lapack_complex_double* dl,
                           lapack_complex_double* d, lapack_complex_double* du,
                           lapack_complex_double* du2, lapack_int* ipiv );

lapack_int LAPACKE_sgttrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const float* dl, const float* d,
                           const float* du, const float* du2,
                           const lapack_int* ipiv, float* b, lapack_int ldb );
lapack_int LAPACKE_dgttrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const double* dl, const double* d,
                           const double* du, const double* du2,
                           const lapack_int* ipiv, double* b, lapack_int ldb );
lapack_int LAPACKE_cgttrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* dl,
                           const lapack_complex_float* d,
                           const lapack_complex_float* du,
                           const lapack_complex_float* du2,
                           const lapack_int* ipiv, lapack_complex_float* b,
                           lapack_int ldb );
lapack_int LAPACKE_zgttrs( int matrix_layout, char trans, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* dl,
                           const lapack_complex_double* d,
                           const lapack_complex_double* du,
                           const lapack_complex_double* du2,
                           const lapack_int* ipiv, lapack_complex_double* b,
                           lapack_int ldb );

lapack_int LAPACKE_chbev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_int kd, lapack_complex_float* ab,
                          lapack_int ldab, float* w, lapack_complex_float* z,
                          lapack_int ldz );
lapack_int LAPACKE_zhbev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_int kd, lapack_complex_double* ab,
                          lapack_int ldab, double* w, lapack_complex_double* z,
                          lapack_int ldz );

lapack_int LAPACKE_chbevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_int kd, lapack_complex_float* ab,
                           lapack_int ldab, float* w, lapack_complex_float* z,
                           lapack_int ldz );
lapack_int LAPACKE_zhbevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_int kd, lapack_complex_double* ab,
                           lapack_int ldab, double* w, lapack_complex_double* z,
                           lapack_int ldz );

lapack_int LAPACKE_chbevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_int kd,
                           lapack_complex_float* ab, lapack_int ldab,
                           lapack_complex_float* q, lapack_int ldq, float vl,
                           float vu, lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, lapack_complex_float* z,
                           lapack_int ldz, lapack_int* ifail );
lapack_int LAPACKE_zhbevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_int kd,
                           lapack_complex_double* ab, lapack_int ldab,
                           lapack_complex_double* q, lapack_int ldq, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w,
                           lapack_complex_double* z, lapack_int ldz,
                           lapack_int* ifail );

lapack_int LAPACKE_chbgst( int matrix_layout, char vect, char uplo, lapack_int n,
                           lapack_int ka, lapack_int kb,
                           lapack_complex_float* ab, lapack_int ldab,
                           const lapack_complex_float* bb, lapack_int ldbb,
                           lapack_complex_float* x, lapack_int ldx );
lapack_int LAPACKE_zhbgst( int matrix_layout, char vect, char uplo, lapack_int n,
                           lapack_int ka, lapack_int kb,
                           lapack_complex_double* ab, lapack_int ldab,
                           const lapack_complex_double* bb, lapack_int ldbb,
                           lapack_complex_double* x, lapack_int ldx );

lapack_int LAPACKE_chbgv( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_int ka, lapack_int kb,
                          lapack_complex_float* ab, lapack_int ldab,
                          lapack_complex_float* bb, lapack_int ldbb, float* w,
                          lapack_complex_float* z, lapack_int ldz );
lapack_int LAPACKE_zhbgv( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_int ka, lapack_int kb,
                          lapack_complex_double* ab, lapack_int ldab,
                          lapack_complex_double* bb, lapack_int ldbb, double* w,
                          lapack_complex_double* z, lapack_int ldz );

lapack_int LAPACKE_chbgvd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_int ka, lapack_int kb,
                           lapack_complex_float* ab, lapack_int ldab,
                           lapack_complex_float* bb, lapack_int ldbb, float* w,
                           lapack_complex_float* z, lapack_int ldz );
lapack_int LAPACKE_zhbgvd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_int ka, lapack_int kb,
                           lapack_complex_double* ab, lapack_int ldab,
                           lapack_complex_double* bb, lapack_int ldbb,
                           double* w, lapack_complex_double* z,
                           lapack_int ldz );

lapack_int LAPACKE_chbgvx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_int ka, lapack_int kb,
                           lapack_complex_float* ab, lapack_int ldab,
                           lapack_complex_float* bb, lapack_int ldbb,
                           lapack_complex_float* q, lapack_int ldq, float vl,
                           float vu, lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, lapack_complex_float* z,
                           lapack_int ldz, lapack_int* ifail );
lapack_int LAPACKE_zhbgvx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_int ka, lapack_int kb,
                           lapack_complex_double* ab, lapack_int ldab,
                           lapack_complex_double* bb, lapack_int ldbb,
                           lapack_complex_double* q, lapack_int ldq, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w,
                           lapack_complex_double* z, lapack_int ldz,
                           lapack_int* ifail );

lapack_int LAPACKE_chbtrd( int matrix_layout, char vect, char uplo, lapack_int n,
                           lapack_int kd, lapack_complex_float* ab,
                           lapack_int ldab, float* d, float* e,
                           lapack_complex_float* q, lapack_int ldq );
lapack_int LAPACKE_zhbtrd( int matrix_layout, char vect, char uplo, lapack_int n,
                           lapack_int kd, lapack_complex_double* ab,
                           lapack_int ldab, double* d, double* e,
                           lapack_complex_double* q, lapack_int ldq );

lapack_int LAPACKE_checon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_float* a, lapack_int lda,
                           const lapack_int* ipiv, float anorm, float* rcond );
lapack_int LAPACKE_zhecon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_double* a, lapack_int lda,
                           const lapack_int* ipiv, double anorm,
                           double* rcond );

lapack_int LAPACKE_cheequb( int matrix_layout, char uplo, lapack_int n,
                            const lapack_complex_float* a, lapack_int lda,
                            float* s, float* scond, float* amax );
lapack_int LAPACKE_zheequb( int matrix_layout, char uplo, lapack_int n,
                            const lapack_complex_double* a, lapack_int lda,
                            double* s, double* scond, double* amax );

lapack_int LAPACKE_cheev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_complex_float* a, lapack_int lda, float* w );
lapack_int LAPACKE_zheev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_complex_double* a, lapack_int lda, double* w );

lapack_int LAPACKE_cheevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda, float* w );
lapack_int LAPACKE_zheevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           double* w );

lapack_int LAPACKE_cheevr( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_complex_float* a,
                           lapack_int lda, float vl, float vu, lapack_int il,
                           lapack_int iu, float abstol, lapack_int* m, float* w,
                           lapack_complex_float* z, lapack_int ldz,
                           lapack_int* isuppz );
lapack_int LAPACKE_zheevr( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_complex_double* a,
                           lapack_int lda, double vl, double vu, lapack_int il,
                           lapack_int iu, double abstol, lapack_int* m,
                           double* w, lapack_complex_double* z, lapack_int ldz,
                           lapack_int* isuppz );

lapack_int LAPACKE_cheevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_complex_float* a,
                           lapack_int lda, float vl, float vu, lapack_int il,
                           lapack_int iu, float abstol, lapack_int* m, float* w,
                           lapack_complex_float* z, lapack_int ldz,
                           lapack_int* ifail );
lapack_int LAPACKE_zheevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_complex_double* a,
                           lapack_int lda, double vl, double vu, lapack_int il,
                           lapack_int iu, double abstol, lapack_int* m,
                           double* w, lapack_complex_double* z, lapack_int ldz,
                           lapack_int* ifail );

lapack_int LAPACKE_chegst( int matrix_layout, lapack_int itype, char uplo,
                           lapack_int n, lapack_complex_float* a,
                           lapack_int lda, const lapack_complex_float* b,
                           lapack_int ldb );
lapack_int LAPACKE_zhegst( int matrix_layout, lapack_int itype, char uplo,
                           lapack_int n, lapack_complex_double* a,
                           lapack_int lda, const lapack_complex_double* b,
                           lapack_int ldb );

lapack_int LAPACKE_chegv( int matrix_layout, lapack_int itype, char jobz,
                          char uplo, lapack_int n, lapack_complex_float* a,
                          lapack_int lda, lapack_complex_float* b,
                          lapack_int ldb, float* w );
lapack_int LAPACKE_zhegv( int matrix_layout, lapack_int itype, char jobz,
                          char uplo, lapack_int n, lapack_complex_double* a,
                          lapack_int lda, lapack_complex_double* b,
                          lapack_int ldb, double* w );

lapack_int LAPACKE_chegvd( int matrix_layout, lapack_int itype, char jobz,
                           char uplo, lapack_int n, lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* b,
                           lapack_int ldb, float* w );
lapack_int LAPACKE_zhegvd( int matrix_layout, lapack_int itype, char jobz,
                           char uplo, lapack_int n, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* b,
                           lapack_int ldb, double* w );

lapack_int LAPACKE_chegvx( int matrix_layout, lapack_int itype, char jobz,
                           char range, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_complex_float* b, lapack_int ldb, float vl,
                           float vu, lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, lapack_complex_float* z,
                           lapack_int ldz, lapack_int* ifail );
lapack_int LAPACKE_zhegvx( int matrix_layout, lapack_int itype, char jobz,
                           char range, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_complex_double* b, lapack_int ldb, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w,
                           lapack_complex_double* z, lapack_int ldz,
                           lapack_int* ifail );

lapack_int LAPACKE_cherfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* a,
                           lapack_int lda, const lapack_complex_float* af,
                           lapack_int ldaf, const lapack_int* ipiv,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx, float* ferr,
                           float* berr );
lapack_int LAPACKE_zherfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* a,
                           lapack_int lda, const lapack_complex_double* af,
                           lapack_int ldaf, const lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* ferr, double* berr );

lapack_int LAPACKE_cherfsx( int matrix_layout, char uplo, char equed,
                            lapack_int n, lapack_int nrhs,
                            const lapack_complex_float* a, lapack_int lda,
                            const lapack_complex_float* af, lapack_int ldaf,
                            const lapack_int* ipiv, const float* s,
                            const lapack_complex_float* b, lapack_int ldb,
                            lapack_complex_float* x, lapack_int ldx,
                            float* rcond, float* berr, lapack_int n_err_bnds,
                            float* err_bnds_norm, float* err_bnds_comp,
                            lapack_int nparams, float* params );
lapack_int LAPACKE_zherfsx( int matrix_layout, char uplo, char equed,
                            lapack_int n, lapack_int nrhs,
                            const lapack_complex_double* a, lapack_int lda,
                            const lapack_complex_double* af, lapack_int ldaf,
                            const lapack_int* ipiv, const double* s,
                            const lapack_complex_double* b, lapack_int ldb,
                            lapack_complex_double* x, lapack_int ldx,
                            double* rcond, double* berr, lapack_int n_err_bnds,
                            double* err_bnds_norm, double* err_bnds_comp,
                            lapack_int nparams, double* params );

lapack_int LAPACKE_chesv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_float* a,
                          lapack_int lda, lapack_int* ipiv,
                          lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zhesv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_double* a,
                          lapack_int lda, lapack_int* ipiv,
                          lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_chesvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* af,
                           lapack_int ldaf, lapack_int* ipiv,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx,
                           float* rcond, float* ferr, float* berr );
lapack_int LAPACKE_zhesvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* af,
                           lapack_int ldaf, lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr );

lapack_int LAPACKE_chesvxx( int matrix_layout, char fact, char uplo,
                            lapack_int n, lapack_int nrhs,
                            lapack_complex_float* a, lapack_int lda,
                            lapack_complex_float* af, lapack_int ldaf,
                            lapack_int* ipiv, char* equed, float* s,
                            lapack_complex_float* b, lapack_int ldb,
                            lapack_complex_float* x, lapack_int ldx,
                            float* rcond, float* rpvgrw, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_zhesvxx( int matrix_layout, char fact, char uplo,
                            lapack_int n, lapack_int nrhs,
                            lapack_complex_double* a, lapack_int lda,
                            lapack_complex_double* af, lapack_int ldaf,
                            lapack_int* ipiv, char* equed, double* s,
                            lapack_complex_double* b, lapack_int ldb,
                            lapack_complex_double* x, lapack_int ldx,
                            double* rcond, double* rpvgrw, double* berr,
                            lapack_int n_err_bnds, double* err_bnds_norm,
                            double* err_bnds_comp, lapack_int nparams,
                            double* params );

lapack_int LAPACKE_chetrd( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda, float* d,
                           float* e, lapack_complex_float* tau );
lapack_int LAPACKE_zhetrd( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda, double* d,
                           double* e, lapack_complex_double* tau );

lapack_int LAPACKE_chetrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int* ipiv );
lapack_int LAPACKE_zhetrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* ipiv );

lapack_int LAPACKE_chetri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           const lapack_int* ipiv );
lapack_int LAPACKE_zhetri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           const lapack_int* ipiv );

lapack_int LAPACKE_chetrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* a,
                           lapack_int lda, const lapack_int* ipiv,
                           lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zhetrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* a,
                           lapack_int lda, const lapack_int* ipiv,
                           lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_chfrk( int matrix_layout, char transr, char uplo, char trans,
                          lapack_int n, lapack_int k, float alpha,
                          const lapack_complex_float* a, lapack_int lda,
                          float beta, lapack_complex_float* c );
lapack_int LAPACKE_zhfrk( int matrix_layout, char transr, char uplo, char trans,
                          lapack_int n, lapack_int k, double alpha,
                          const lapack_complex_double* a, lapack_int lda,
                          double beta, lapack_complex_double* c );

lapack_int LAPACKE_shgeqz( int matrix_layout, char job, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           float* h, lapack_int ldh, float* t, lapack_int ldt,
                           float* alphar, float* alphai, float* beta, float* q,
                           lapack_int ldq, float* z, lapack_int ldz );
lapack_int LAPACKE_dhgeqz( int matrix_layout, char job, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           double* h, lapack_int ldh, double* t, lapack_int ldt,
                           double* alphar, double* alphai, double* beta,
                           double* q, lapack_int ldq, double* z,
                           lapack_int ldz );
lapack_int LAPACKE_chgeqz( int matrix_layout, char job, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           lapack_complex_float* h, lapack_int ldh,
                           lapack_complex_float* t, lapack_int ldt,
                           lapack_complex_float* alpha,
                           lapack_complex_float* beta, lapack_complex_float* q,
                           lapack_int ldq, lapack_complex_float* z,
                           lapack_int ldz );
lapack_int LAPACKE_zhgeqz( int matrix_layout, char job, char compq, char compz,
                           lapack_int n, lapack_int ilo, lapack_int ihi,
                           lapack_complex_double* h, lapack_int ldh,
                           lapack_complex_double* t, lapack_int ldt,
                           lapack_complex_double* alpha,
                           lapack_complex_double* beta,
                           lapack_complex_double* q, lapack_int ldq,
                           lapack_complex_double* z, lapack_int ldz );

lapack_int LAPACKE_chpcon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_float* ap,
                           const lapack_int* ipiv, float anorm, float* rcond );
lapack_int LAPACKE_zhpcon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_double* ap,
                           const lapack_int* ipiv, double anorm,
                           double* rcond );

lapack_int LAPACKE_chpev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_complex_float* ap, float* w,
                          lapack_complex_float* z, lapack_int ldz );
lapack_int LAPACKE_zhpev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_complex_double* ap, double* w,
                          lapack_complex_double* z, lapack_int ldz );

lapack_int LAPACKE_chpevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_complex_float* ap, float* w,
                           lapack_complex_float* z, lapack_int ldz );
lapack_int LAPACKE_zhpevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_complex_double* ap, double* w,
                           lapack_complex_double* z, lapack_int ldz );

lapack_int LAPACKE_chpevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_complex_float* ap, float vl,
                           float vu, lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, lapack_complex_float* z,
                           lapack_int ldz, lapack_int* ifail );
lapack_int LAPACKE_zhpevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_complex_double* ap, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w,
                           lapack_complex_double* z, lapack_int ldz,
                           lapack_int* ifail );

lapack_int LAPACKE_chpgst( int matrix_layout, lapack_int itype, char uplo,
                           lapack_int n, lapack_complex_float* ap,
                           const lapack_complex_float* bp );
lapack_int LAPACKE_zhpgst( int matrix_layout, lapack_int itype, char uplo,
                           lapack_int n, lapack_complex_double* ap,
                           const lapack_complex_double* bp );

lapack_int LAPACKE_chpgv( int matrix_layout, lapack_int itype, char jobz,
                          char uplo, lapack_int n, lapack_complex_float* ap,
                          lapack_complex_float* bp, float* w,
                          lapack_complex_float* z, lapack_int ldz );
lapack_int LAPACKE_zhpgv( int matrix_layout, lapack_int itype, char jobz,
                          char uplo, lapack_int n, lapack_complex_double* ap,
                          lapack_complex_double* bp, double* w,
                          lapack_complex_double* z, lapack_int ldz );

lapack_int LAPACKE_chpgvd( int matrix_layout, lapack_int itype, char jobz,
                           char uplo, lapack_int n, lapack_complex_float* ap,
                           lapack_complex_float* bp, float* w,
                           lapack_complex_float* z, lapack_int ldz );
lapack_int LAPACKE_zhpgvd( int matrix_layout, lapack_int itype, char jobz,
                           char uplo, lapack_int n, lapack_complex_double* ap,
                           lapack_complex_double* bp, double* w,
                           lapack_complex_double* z, lapack_int ldz );

lapack_int LAPACKE_chpgvx( int matrix_layout, lapack_int itype, char jobz,
                           char range, char uplo, lapack_int n,
                           lapack_complex_float* ap, lapack_complex_float* bp,
                           float vl, float vu, lapack_int il, lapack_int iu,
                           float abstol, lapack_int* m, float* w,
                           lapack_complex_float* z, lapack_int ldz,
                           lapack_int* ifail );
lapack_int LAPACKE_zhpgvx( int matrix_layout, lapack_int itype, char jobz,
                           char range, char uplo, lapack_int n,
                           lapack_complex_double* ap, lapack_complex_double* bp,
                           double vl, double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w,
                           lapack_complex_double* z, lapack_int ldz,
                           lapack_int* ifail );

lapack_int LAPACKE_chprfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* ap,
                           const lapack_complex_float* afp,
                           const lapack_int* ipiv,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx, float* ferr,
                           float* berr );
lapack_int LAPACKE_zhprfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* ap,
                           const lapack_complex_double* afp,
                           const lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* ferr, double* berr );

lapack_int LAPACKE_chpsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_float* ap,
                          lapack_int* ipiv, lapack_complex_float* b,
                          lapack_int ldb );
lapack_int LAPACKE_zhpsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_double* ap,
                          lapack_int* ipiv, lapack_complex_double* b,
                          lapack_int ldb );

lapack_int LAPACKE_chpsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* ap,
                           lapack_complex_float* afp, lapack_int* ipiv,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx,
                           float* rcond, float* ferr, float* berr );
lapack_int LAPACKE_zhpsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* ap,
                           lapack_complex_double* afp, lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr );

lapack_int LAPACKE_chptrd( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* ap, float* d, float* e,
                           lapack_complex_float* tau );
lapack_int LAPACKE_zhptrd( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* ap, double* d, double* e,
                           lapack_complex_double* tau );

lapack_int LAPACKE_chptrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* ap, lapack_int* ipiv );
lapack_int LAPACKE_zhptrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* ap, lapack_int* ipiv );

lapack_int LAPACKE_chptri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* ap, const lapack_int* ipiv );
lapack_int LAPACKE_zhptri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* ap, const lapack_int* ipiv );

lapack_int LAPACKE_chptrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* ap,
                           const lapack_int* ipiv, lapack_complex_float* b,
                           lapack_int ldb );
lapack_int LAPACKE_zhptrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* ap,
                           const lapack_int* ipiv, lapack_complex_double* b,
                           lapack_int ldb );

lapack_int LAPACKE_shsein( int matrix_layout, char job, char eigsrc, char initv,
                           lapack_logical* select, lapack_int n, const float* h,
                           lapack_int ldh, float* wr, const float* wi,
                           float* vl, lapack_int ldvl, float* vr,
                           lapack_int ldvr, lapack_int mm, lapack_int* m,
                           lapack_int* ifaill, lapack_int* ifailr );
lapack_int LAPACKE_dhsein( int matrix_layout, char job, char eigsrc, char initv,
                           lapack_logical* select, lapack_int n,
                           const double* h, lapack_int ldh, double* wr,
                           const double* wi, double* vl, lapack_int ldvl,
                           double* vr, lapack_int ldvr, lapack_int mm,
                           lapack_int* m, lapack_int* ifaill,
                           lapack_int* ifailr );
lapack_int LAPACKE_chsein( int matrix_layout, char job, char eigsrc, char initv,
                           const lapack_logical* select, lapack_int n,
                           const lapack_complex_float* h, lapack_int ldh,
                           lapack_complex_float* w, lapack_complex_float* vl,
                           lapack_int ldvl, lapack_complex_float* vr,
                           lapack_int ldvr, lapack_int mm, lapack_int* m,
                           lapack_int* ifaill, lapack_int* ifailr );
lapack_int LAPACKE_zhsein( int matrix_layout, char job, char eigsrc, char initv,
                           const lapack_logical* select, lapack_int n,
                           const lapack_complex_double* h, lapack_int ldh,
                           lapack_complex_double* w, lapack_complex_double* vl,
                           lapack_int ldvl, lapack_complex_double* vr,
                           lapack_int ldvr, lapack_int mm, lapack_int* m,
                           lapack_int* ifaill, lapack_int* ifailr );

lapack_int LAPACKE_shseqr( int matrix_layout, char job, char compz, lapack_int n,
                           lapack_int ilo, lapack_int ihi, float* h,
                           lapack_int ldh, float* wr, float* wi, float* z,
                           lapack_int ldz );
lapack_int LAPACKE_dhseqr( int matrix_layout, char job, char compz, lapack_int n,
                           lapack_int ilo, lapack_int ihi, double* h,
                           lapack_int ldh, double* wr, double* wi, double* z,
                           lapack_int ldz );
lapack_int LAPACKE_chseqr( int matrix_layout, char job, char compz, lapack_int n,
                           lapack_int ilo, lapack_int ihi,
                           lapack_complex_float* h, lapack_int ldh,
                           lapack_complex_float* w, lapack_complex_float* z,
                           lapack_int ldz );
lapack_int LAPACKE_zhseqr( int matrix_layout, char job, char compz, lapack_int n,
                           lapack_int ilo, lapack_int ihi,
                           lapack_complex_double* h, lapack_int ldh,
                           lapack_complex_double* w, lapack_complex_double* z,
                           lapack_int ldz );

lapack_int LAPACKE_clacgv( lapack_int n, lapack_complex_float* x,
                           lapack_int incx );
lapack_int LAPACKE_zlacgv( lapack_int n, lapack_complex_double* x,
                           lapack_int incx );

lapack_int LAPACKE_slacn2( lapack_int n, float* v, float* x, lapack_int* isgn,
                           float* est, lapack_int* kase, lapack_int* isave );
lapack_int LAPACKE_dlacn2( lapack_int n, double* v, double* x, lapack_int* isgn,
                           double* est, lapack_int* kase, lapack_int* isave );
lapack_int LAPACKE_clacn2( lapack_int n, lapack_complex_float* v,
                           lapack_complex_float* x,
                           float* est, lapack_int* kase, lapack_int* isave );
lapack_int LAPACKE_zlacn2( lapack_int n, lapack_complex_double* v,
                           lapack_complex_double* x,
                           double* est, lapack_int* kase, lapack_int* isave );

lapack_int LAPACKE_slacpy( int matrix_layout, char uplo, lapack_int m,
                           lapack_int n, const float* a, lapack_int lda, float* b,
                           lapack_int ldb );
lapack_int LAPACKE_dlacpy( int matrix_layout, char uplo, lapack_int m,
                           lapack_int n, const double* a, lapack_int lda, double* b,
                           lapack_int ldb );
lapack_int LAPACKE_clacpy( int matrix_layout, char uplo, lapack_int m,
                           lapack_int n, const lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* b,
                           lapack_int ldb );
lapack_int LAPACKE_zlacpy( int matrix_layout, char uplo, lapack_int m,
                           lapack_int n, const lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* b,
                           lapack_int ldb );

lapack_int LAPACKE_clacp2( int matrix_layout, char uplo, lapack_int m,
                           lapack_int n, const float* a, lapack_int lda,
                           lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zlacp2( int matrix_layout, char uplo, lapack_int m,
                           lapack_int n, const double* a, lapack_int lda,
                           lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_zlag2c( int matrix_layout, lapack_int m, lapack_int n,
                           const lapack_complex_double* a, lapack_int lda,
                           lapack_complex_float* sa, lapack_int ldsa );

lapack_int LAPACKE_slag2d( int matrix_layout, lapack_int m, lapack_int n,
                           const float* sa, lapack_int ldsa, double* a,
                           lapack_int lda );

lapack_int LAPACKE_dlag2s( int matrix_layout, lapack_int m, lapack_int n,
                           const double* a, lapack_int lda, float* sa,
                           lapack_int ldsa );

lapack_int LAPACKE_clag2z( int matrix_layout, lapack_int m, lapack_int n,
                           const lapack_complex_float* sa, lapack_int ldsa,
                           lapack_complex_double* a, lapack_int lda );

lapack_int LAPACKE_slagge( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku, const float* d,
                           float* a, lapack_int lda, lapack_int* iseed );
lapack_int LAPACKE_dlagge( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku, const double* d,
                           double* a, lapack_int lda, lapack_int* iseed );
lapack_int LAPACKE_clagge( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku, const float* d,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int* iseed );
lapack_int LAPACKE_zlagge( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int kl, lapack_int ku, const double* d,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* iseed );

float LAPACKE_slamch( char cmach );
double LAPACKE_dlamch( char cmach );

float LAPACKE_slange( int matrix_layout, char norm, lapack_int m,
                           lapack_int n, const float* a, lapack_int lda );
double LAPACKE_dlange( int matrix_layout, char norm, lapack_int m,
                           lapack_int n, const double* a, lapack_int lda );
float LAPACKE_clange( int matrix_layout, char norm, lapack_int m,
                           lapack_int n, const lapack_complex_float* a,
                           lapack_int lda );
double LAPACKE_zlange( int matrix_layout, char norm, lapack_int m,
                           lapack_int n, const lapack_complex_double* a,
                           lapack_int lda );

float LAPACKE_clanhe( int matrix_layout, char norm, char uplo, lapack_int n,
                           const lapack_complex_float* a, lapack_int lda );
double LAPACKE_zlanhe( int matrix_layout, char norm, char uplo, lapack_int n,
                           const lapack_complex_double* a, lapack_int lda );

lapack_int LAPACKE_clacrm( int matrix_layout, lapack_int m, lapack_int n,
                          const lapack_complex_float* a,
                          lapack_int lda, const float* b,
                          lapack_int ldb, lapack_complex_float* c,
                          lapack_int ldc );
lapack_int LAPACKE_zlacrm( int matrix_layout, lapack_int m, lapack_int n,
                           const lapack_complex_double* a,
                           lapack_int lda, const double* b,
                           lapack_int ldb, lapack_complex_double* c,
                           lapack_int ldc );

lapack_int LAPACKE_clarcm( int matrix_layout, lapack_int m, lapack_int n,
                          const float* a, lapack_int lda,
                          const lapack_complex_float* b,
                          lapack_int ldb, lapack_complex_float* c,
                          lapack_int ldc );
lapack_int LAPACKE_zlarcm( int matrix_layout, lapack_int m, lapack_int n,
                           const double* a, lapack_int lda,
                           const lapack_complex_double* b,
                           lapack_int ldb, lapack_complex_double* c,
                           lapack_int ldc );

float LAPACKE_slansy( int matrix_layout, char norm, char uplo, lapack_int n,
                           const float* a, lapack_int lda );
double LAPACKE_dlansy( int matrix_layout, char norm, char uplo, lapack_int n,
                           const double* a, lapack_int lda );
float LAPACKE_clansy( int matrix_layout, char norm, char uplo, lapack_int n,
                           const lapack_complex_float* a, lapack_int lda );
double LAPACKE_zlansy( int matrix_layout, char norm, char uplo, lapack_int n,
                           const lapack_complex_double* a, lapack_int lda );

float LAPACKE_slantr( int matrix_layout, char norm, char uplo, char diag,
                           lapack_int m, lapack_int n, const float* a,
                           lapack_int lda );
double LAPACKE_dlantr( int matrix_layout, char norm, char uplo, char diag,
                           lapack_int m, lapack_int n, const double* a,
                           lapack_int lda );
float LAPACKE_clantr( int matrix_layout, char norm, char uplo, char diag,
                           lapack_int m, lapack_int n, const lapack_complex_float* a,
                           lapack_int lda );
double LAPACKE_zlantr( int matrix_layout, char norm, char uplo, char diag,
                           lapack_int m, lapack_int n, const lapack_complex_double* a,
                           lapack_int lda );


lapack_int LAPACKE_slarfb( int matrix_layout, char side, char trans, char direct,
                           char storev, lapack_int m, lapack_int n,
                           lapack_int k, const float* v, lapack_int ldv,
                           const float* t, lapack_int ldt, float* c,
                           lapack_int ldc );
lapack_int LAPACKE_dlarfb( int matrix_layout, char side, char trans, char direct,
                           char storev, lapack_int m, lapack_int n,
                           lapack_int k, const double* v, lapack_int ldv,
                           const double* t, lapack_int ldt, double* c,
                           lapack_int ldc );
lapack_int LAPACKE_clarfb( int matrix_layout, char side, char trans, char direct,
                           char storev, lapack_int m, lapack_int n,
                           lapack_int k, const lapack_complex_float* v,
                           lapack_int ldv, const lapack_complex_float* t,
                           lapack_int ldt, lapack_complex_float* c,
                           lapack_int ldc );
lapack_int LAPACKE_zlarfb( int matrix_layout, char side, char trans, char direct,
                           char storev, lapack_int m, lapack_int n,
                           lapack_int k, const lapack_complex_double* v,
                           lapack_int ldv, const lapack_complex_double* t,
                           lapack_int ldt, lapack_complex_double* c,
                           lapack_int ldc );

lapack_int LAPACKE_slarfg( lapack_int n, float* alpha, float* x,
                           lapack_int incx, float* tau );
lapack_int LAPACKE_dlarfg( lapack_int n, double* alpha, double* x,
                           lapack_int incx, double* tau );
lapack_int LAPACKE_clarfg( lapack_int n, lapack_complex_float* alpha,
                           lapack_complex_float* x, lapack_int incx,
                           lapack_complex_float* tau );
lapack_int LAPACKE_zlarfg( lapack_int n, lapack_complex_double* alpha,
                           lapack_complex_double* x, lapack_int incx,
                           lapack_complex_double* tau );

lapack_int LAPACKE_slarft( int matrix_layout, char direct, char storev,
                           lapack_int n, lapack_int k, const float* v,
                           lapack_int ldv, const float* tau, float* t,
                           lapack_int ldt );
lapack_int LAPACKE_dlarft( int matrix_layout, char direct, char storev,
                           lapack_int n, lapack_int k, const double* v,
                           lapack_int ldv, const double* tau, double* t,
                           lapack_int ldt );
lapack_int LAPACKE_clarft( int matrix_layout, char direct, char storev,
                           lapack_int n, lapack_int k,
                           const lapack_complex_float* v, lapack_int ldv,
                           const lapack_complex_float* tau,
                           lapack_complex_float* t, lapack_int ldt );
lapack_int LAPACKE_zlarft( int matrix_layout, char direct, char storev,
                           lapack_int n, lapack_int k,
                           const lapack_complex_double* v, lapack_int ldv,
                           const lapack_complex_double* tau,
                           lapack_complex_double* t, lapack_int ldt );

lapack_int LAPACKE_slarfx( int matrix_layout, char side, lapack_int m,
                           lapack_int n, const float* v, float tau, float* c,
                           lapack_int ldc, float* work );
lapack_int LAPACKE_dlarfx( int matrix_layout, char side, lapack_int m,
                           lapack_int n, const double* v, double tau, double* c,
                           lapack_int ldc, double* work );
lapack_int LAPACKE_clarfx( int matrix_layout, char side, lapack_int m,
                           lapack_int n, const lapack_complex_float* v,
                           lapack_complex_float tau, lapack_complex_float* c,
                           lapack_int ldc, lapack_complex_float* work );
lapack_int LAPACKE_zlarfx( int matrix_layout, char side, lapack_int m,
                           lapack_int n, const lapack_complex_double* v,
                           lapack_complex_double tau, lapack_complex_double* c,
                           lapack_int ldc, lapack_complex_double* work );

lapack_int LAPACKE_slarnv( lapack_int idist, lapack_int* iseed, lapack_int n,
                           float* x );
lapack_int LAPACKE_dlarnv( lapack_int idist, lapack_int* iseed, lapack_int n,
                           double* x );
lapack_int LAPACKE_clarnv( lapack_int idist, lapack_int* iseed, lapack_int n,
                           lapack_complex_float* x );
lapack_int LAPACKE_zlarnv( lapack_int idist, lapack_int* iseed, lapack_int n,
                           lapack_complex_double* x );

lapack_int LAPACKE_slascl( int matrix_layout, char type, lapack_int kl,
                           lapack_int ku, float cfrom, float cto,
                           lapack_int m, lapack_int n, float* a,
                           lapack_int lda );
lapack_int LAPACKE_dlascl( int matrix_layout, char type, lapack_int kl,
                           lapack_int ku, double cfrom, double cto,
                           lapack_int m, lapack_int n, double* a,
                           lapack_int lda );
lapack_int LAPACKE_clascl( int matrix_layout, char type, lapack_int kl,
                           lapack_int ku, float cfrom, float cto,
                           lapack_int m, lapack_int n, lapack_complex_float* a,
                           lapack_int lda );
lapack_int LAPACKE_zlascl( int matrix_layout, char type, lapack_int kl,
                           lapack_int ku, double cfrom, double cto,
                           lapack_int m, lapack_int n, lapack_complex_double* a,
                           lapack_int lda );

lapack_int LAPACKE_slaset( int matrix_layout, char uplo, lapack_int m,
                           lapack_int n, float alpha, float beta, float* a,
                           lapack_int lda );
lapack_int LAPACKE_dlaset( int matrix_layout, char uplo, lapack_int m,
                           lapack_int n, double alpha, double beta, double* a,
                           lapack_int lda );
lapack_int LAPACKE_claset( int matrix_layout, char uplo, lapack_int m,
                           lapack_int n, lapack_complex_float alpha,
                           lapack_complex_float beta, lapack_complex_float* a,
                           lapack_int lda );
lapack_int LAPACKE_zlaset( int matrix_layout, char uplo, lapack_int m,
                           lapack_int n, lapack_complex_double alpha,
                           lapack_complex_double beta, lapack_complex_double* a,
                           lapack_int lda );

lapack_int LAPACKE_slasrt( char id, lapack_int n, float* d );
lapack_int LAPACKE_dlasrt( char id, lapack_int n, double* d );

lapack_int LAPACKE_slassq( lapack_int n,                 float* x, lapack_int incx,  float* scale,  float* sumsq );
lapack_int LAPACKE_dlassq( lapack_int n,                double* x, lapack_int incx, double* scale, double* sumsq );
lapack_int LAPACKE_classq( lapack_int n,  lapack_complex_float* x, lapack_int incx,  float* scale,  float* sumsq );
lapack_int LAPACKE_zlassq( lapack_int n, lapack_complex_double* x, lapack_int incx, double* scale, double* sumsq );

lapack_int LAPACKE_slaswp( int matrix_layout, lapack_int n, float* a,
                           lapack_int lda, lapack_int k1, lapack_int k2,
                           const lapack_int* ipiv, lapack_int incx );
lapack_int LAPACKE_dlaswp( int matrix_layout, lapack_int n, double* a,
                           lapack_int lda, lapack_int k1, lapack_int k2,
                           const lapack_int* ipiv, lapack_int incx );
lapack_int LAPACKE_claswp( int matrix_layout, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int k1, lapack_int k2, const lapack_int* ipiv,
                           lapack_int incx );
lapack_int LAPACKE_zlaswp( int matrix_layout, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int k1, lapack_int k2, const lapack_int* ipiv,
                           lapack_int incx );

lapack_int LAPACKE_slatms( int matrix_layout, lapack_int m, lapack_int n,
                           char dist, lapack_int* iseed, char sym, float* d,
                           lapack_int mode, float cond, float dmax,
                           lapack_int kl, lapack_int ku, char pack, float* a,
                           lapack_int lda );
lapack_int LAPACKE_dlatms( int matrix_layout, lapack_int m, lapack_int n,
                           char dist, lapack_int* iseed, char sym, double* d,
                           lapack_int mode, double cond, double dmax,
                           lapack_int kl, lapack_int ku, char pack, double* a,
                           lapack_int lda );
lapack_int LAPACKE_clatms( int matrix_layout, lapack_int m, lapack_int n,
                           char dist, lapack_int* iseed, char sym, float* d,
                           lapack_int mode, float cond, float dmax,
                           lapack_int kl, lapack_int ku, char pack,
                           lapack_complex_float* a, lapack_int lda );
lapack_int LAPACKE_zlatms( int matrix_layout, lapack_int m, lapack_int n,
                           char dist, lapack_int* iseed, char sym, double* d,
                           lapack_int mode, double cond, double dmax,
                           lapack_int kl, lapack_int ku, char pack,
                           lapack_complex_double* a, lapack_int lda );

lapack_int LAPACKE_slauum( int matrix_layout, char uplo, lapack_int n, float* a,
                           lapack_int lda );
lapack_int LAPACKE_dlauum( int matrix_layout, char uplo, lapack_int n, double* a,
                           lapack_int lda );
lapack_int LAPACKE_clauum( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda );
lapack_int LAPACKE_zlauum( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda );

lapack_int LAPACKE_sopgtr( int matrix_layout, char uplo, lapack_int n,
                           const float* ap, const float* tau, float* q,
                           lapack_int ldq );
lapack_int LAPACKE_dopgtr( int matrix_layout, char uplo, lapack_int n,
                           const double* ap, const double* tau, double* q,
                           lapack_int ldq );

lapack_int LAPACKE_sopmtr( int matrix_layout, char side, char uplo, char trans,
                           lapack_int m, lapack_int n, const float* ap,
                           const float* tau, float* c, lapack_int ldc );
lapack_int LAPACKE_dopmtr( int matrix_layout, char side, char uplo, char trans,
                           lapack_int m, lapack_int n, const double* ap,
                           const double* tau, double* c, lapack_int ldc );

lapack_int LAPACKE_sorgbr( int matrix_layout, char vect, lapack_int m,
                           lapack_int n, lapack_int k, float* a, lapack_int lda,
                           const float* tau );
lapack_int LAPACKE_dorgbr( int matrix_layout, char vect, lapack_int m,
                           lapack_int n, lapack_int k, double* a,
                           lapack_int lda, const double* tau );

lapack_int LAPACKE_sorghr( int matrix_layout, lapack_int n, lapack_int ilo,
                           lapack_int ihi, float* a, lapack_int lda,
                           const float* tau );
lapack_int LAPACKE_dorghr( int matrix_layout, lapack_int n, lapack_int ilo,
                           lapack_int ihi, double* a, lapack_int lda,
                           const double* tau );

lapack_int LAPACKE_sorglq( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int k, float* a, lapack_int lda,
                           const float* tau );
lapack_int LAPACKE_dorglq( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int k, double* a, lapack_int lda,
                           const double* tau );

lapack_int LAPACKE_sorgql( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int k, float* a, lapack_int lda,
                           const float* tau );
lapack_int LAPACKE_dorgql( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int k, double* a, lapack_int lda,
                           const double* tau );

lapack_int LAPACKE_sorgqr( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int k, float* a, lapack_int lda,
                           const float* tau );
lapack_int LAPACKE_dorgqr( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int k, double* a, lapack_int lda,
                           const double* tau );

lapack_int LAPACKE_sorgrq( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int k, float* a, lapack_int lda,
                           const float* tau );
lapack_int LAPACKE_dorgrq( int matrix_layout, lapack_int m, lapack_int n,
                           lapack_int k, double* a, lapack_int lda,
                           const double* tau );

lapack_int LAPACKE_sorgtr( int matrix_layout, char uplo, lapack_int n, float* a,
                           lapack_int lda, const float* tau );
lapack_int LAPACKE_dorgtr( int matrix_layout, char uplo, lapack_int n, double* a,
                           lapack_int lda, const double* tau );

lapack_int LAPACKE_sorgtsqr_row( int matrix_layout, lapack_int m, lapack_int n,
                                 lapack_int mb, lapack_int nb,
                                 float* a, lapack_int lda,
                                 const float* t, lapack_int ldt );
lapack_int LAPACKE_dorgtsqr_row( int matrix_layout, lapack_int m, lapack_int n,
                                 lapack_int mb, lapack_int nb,
                                 double* a, lapack_int lda,
                                 const double* t, lapack_int ldt );

lapack_int LAPACKE_sormbr( int matrix_layout, char vect, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           const float* a, lapack_int lda, const float* tau,
                           float* c, lapack_int ldc );
lapack_int LAPACKE_dormbr( int matrix_layout, char vect, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           const double* a, lapack_int lda, const double* tau,
                           double* c, lapack_int ldc );

lapack_int LAPACKE_sormhr( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int ilo,
                           lapack_int ihi, const float* a, lapack_int lda,
                           const float* tau, float* c, lapack_int ldc );
lapack_int LAPACKE_dormhr( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int ilo,
                           lapack_int ihi, const double* a, lapack_int lda,
                           const double* tau, double* c, lapack_int ldc );

lapack_int LAPACKE_sormlq( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           const float* a, lapack_int lda, const float* tau,
                           float* c, lapack_int ldc );
lapack_int LAPACKE_dormlq( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           const double* a, lapack_int lda, const double* tau,
                           double* c, lapack_int ldc );

lapack_int LAPACKE_sormql( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           const float* a, lapack_int lda, const float* tau,
                           float* c, lapack_int ldc );
lapack_int LAPACKE_dormql( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           const double* a, lapack_int lda, const double* tau,
                           double* c, lapack_int ldc );

lapack_int LAPACKE_sormqr( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           const float* a, lapack_int lda, const float* tau,
                           float* c, lapack_int ldc );
lapack_int LAPACKE_dormqr( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           const double* a, lapack_int lda, const double* tau,
                           double* c, lapack_int ldc );

lapack_int LAPACKE_sormrq( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           const float* a, lapack_int lda, const float* tau,
                           float* c, lapack_int ldc );
lapack_int LAPACKE_dormrq( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           const double* a, lapack_int lda, const double* tau,
                           double* c, lapack_int ldc );

lapack_int LAPACKE_sormrz( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           lapack_int l, const float* a, lapack_int lda,
                           const float* tau, float* c, lapack_int ldc );
lapack_int LAPACKE_dormrz( int matrix_layout, char side, char trans,
                           lapack_int m, lapack_int n, lapack_int k,
                           lapack_int l, const double* a, lapack_int lda,
                           const double* tau, double* c, lapack_int ldc );

lapack_int LAPACKE_sormtr( int matrix_layout, char side, char uplo, char trans,
                           lapack_int m, lapack_int n, const float* a,
                           lapack_int lda, const float* tau, float* c,
                           lapack_int ldc );
lapack_int LAPACKE_dormtr( int matrix_layout, char side, char uplo, char trans,
                           lapack_int m, lapack_int n, const double* a,
                           lapack_int lda, const double* tau, double* c,
                           lapack_int ldc );

lapack_int LAPACKE_spbcon( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, const float* ab, lapack_int ldab,
                           float anorm, float* rcond );
lapack_int LAPACKE_dpbcon( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, const double* ab, lapack_int ldab,
                           double anorm, double* rcond );
lapack_int LAPACKE_cpbcon( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, const lapack_complex_float* ab,
                           lapack_int ldab, float anorm, float* rcond );
lapack_int LAPACKE_zpbcon( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, const lapack_complex_double* ab,
                           lapack_int ldab, double anorm, double* rcond );

lapack_int LAPACKE_spbequ( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, const float* ab, lapack_int ldab,
                           float* s, float* scond, float* amax );
lapack_int LAPACKE_dpbequ( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, const double* ab, lapack_int ldab,
                           double* s, double* scond, double* amax );
lapack_int LAPACKE_cpbequ( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, const lapack_complex_float* ab,
                           lapack_int ldab, float* s, float* scond,
                           float* amax );
lapack_int LAPACKE_zpbequ( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, const lapack_complex_double* ab,
                           lapack_int ldab, double* s, double* scond,
                           double* amax );

lapack_int LAPACKE_spbrfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs, const float* ab,
                           lapack_int ldab, const float* afb, lapack_int ldafb,
                           const float* b, lapack_int ldb, float* x,
                           lapack_int ldx, float* ferr, float* berr );
lapack_int LAPACKE_dpbrfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs, const double* ab,
                           lapack_int ldab, const double* afb, lapack_int ldafb,
                           const double* b, lapack_int ldb, double* x,
                           lapack_int ldx, double* ferr, double* berr );
lapack_int LAPACKE_cpbrfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs,
                           const lapack_complex_float* ab, lapack_int ldab,
                           const lapack_complex_float* afb, lapack_int ldafb,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx, float* ferr,
                           float* berr );
lapack_int LAPACKE_zpbrfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs,
                           const lapack_complex_double* ab, lapack_int ldab,
                           const lapack_complex_double* afb, lapack_int ldafb,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* ferr, double* berr );

lapack_int LAPACKE_spbstf( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kb, float* bb, lapack_int ldbb );
lapack_int LAPACKE_dpbstf( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kb, double* bb, lapack_int ldbb );
lapack_int LAPACKE_cpbstf( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kb, lapack_complex_float* bb,
                           lapack_int ldbb );
lapack_int LAPACKE_zpbstf( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kb, lapack_complex_double* bb,
                           lapack_int ldbb );

lapack_int LAPACKE_spbsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int kd, lapack_int nrhs, float* ab,
                          lapack_int ldab, float* b, lapack_int ldb );
lapack_int LAPACKE_dpbsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int kd, lapack_int nrhs, double* ab,
                          lapack_int ldab, double* b, lapack_int ldb );
lapack_int LAPACKE_cpbsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int kd, lapack_int nrhs,
                          lapack_complex_float* ab, lapack_int ldab,
                          lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zpbsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int kd, lapack_int nrhs,
                          lapack_complex_double* ab, lapack_int ldab,
                          lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_spbsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs, float* ab,
                           lapack_int ldab, float* afb, lapack_int ldafb,
                           char* equed, float* s, float* b, lapack_int ldb,
                           float* x, lapack_int ldx, float* rcond, float* ferr,
                           float* berr );
lapack_int LAPACKE_dpbsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs, double* ab,
                           lapack_int ldab, double* afb, lapack_int ldafb,
                           char* equed, double* s, double* b, lapack_int ldb,
                           double* x, lapack_int ldx, double* rcond,
                           double* ferr, double* berr );
lapack_int LAPACKE_cpbsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs,
                           lapack_complex_float* ab, lapack_int ldab,
                           lapack_complex_float* afb, lapack_int ldafb,
                           char* equed, float* s, lapack_complex_float* b,
                           lapack_int ldb, lapack_complex_float* x,
                           lapack_int ldx, float* rcond, float* ferr,
                           float* berr );
lapack_int LAPACKE_zpbsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs,
                           lapack_complex_double* ab, lapack_int ldab,
                           lapack_complex_double* afb, lapack_int ldafb,
                           char* equed, double* s, lapack_complex_double* b,
                           lapack_int ldb, lapack_complex_double* x,
                           lapack_int ldx, double* rcond, double* ferr,
                           double* berr );

lapack_int LAPACKE_spbtrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, float* ab, lapack_int ldab );
lapack_int LAPACKE_dpbtrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, double* ab, lapack_int ldab );
lapack_int LAPACKE_cpbtrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, lapack_complex_float* ab,
                           lapack_int ldab );
lapack_int LAPACKE_zpbtrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, lapack_complex_double* ab,
                           lapack_int ldab );

lapack_int LAPACKE_spbtrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs, const float* ab,
                           lapack_int ldab, float* b, lapack_int ldb );
lapack_int LAPACKE_dpbtrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs, const double* ab,
                           lapack_int ldab, double* b, lapack_int ldb );
lapack_int LAPACKE_cpbtrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs,
                           const lapack_complex_float* ab, lapack_int ldab,
                           lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zpbtrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int kd, lapack_int nrhs,
                           const lapack_complex_double* ab, lapack_int ldab,
                           lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_spftrf( int matrix_layout, char transr, char uplo,
                           lapack_int n, float* a );
lapack_int LAPACKE_dpftrf( int matrix_layout, char transr, char uplo,
                           lapack_int n, double* a );
lapack_int LAPACKE_cpftrf( int matrix_layout, char transr, char uplo,
                           lapack_int n, lapack_complex_float* a );
lapack_int LAPACKE_zpftrf( int matrix_layout, char transr, char uplo,
                           lapack_int n, lapack_complex_double* a );

lapack_int LAPACKE_spftri( int matrix_layout, char transr, char uplo,
                           lapack_int n, float* a );
lapack_int LAPACKE_dpftri( int matrix_layout, char transr, char uplo,
                           lapack_int n, double* a );
lapack_int LAPACKE_cpftri( int matrix_layout, char transr, char uplo,
                           lapack_int n, lapack_complex_float* a );
lapack_int LAPACKE_zpftri( int matrix_layout, char transr, char uplo,
                           lapack_int n, lapack_complex_double* a );

lapack_int LAPACKE_spftrs( int matrix_layout, char transr, char uplo,
                           lapack_int n, lapack_int nrhs, const float* a,
                           float* b, lapack_int ldb );
lapack_int LAPACKE_dpftrs( int matrix_layout, char transr, char uplo,
                           lapack_int n, lapack_int nrhs, const double* a,
                           double* b, lapack_int ldb );
lapack_int LAPACKE_cpftrs( int matrix_layout, char transr, char uplo,
                           lapack_int n, lapack_int nrhs,
                           const lapack_complex_float* a,
                           lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zpftrs( int matrix_layout, char transr, char uplo,
                           lapack_int n, lapack_int nrhs,
                           const lapack_complex_double* a,
                           lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_spocon( int matrix_layout, char uplo, lapack_int n,
                           const float* a, lapack_int lda, float anorm,
                           float* rcond );
lapack_int LAPACKE_dpocon( int matrix_layout, char uplo, lapack_int n,
                           const double* a, lapack_int lda, double anorm,
                           double* rcond );
lapack_int LAPACKE_cpocon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_float* a, lapack_int lda,
                           float anorm, float* rcond );
lapack_int LAPACKE_zpocon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_double* a, lapack_int lda,
                           double anorm, double* rcond );

lapack_int LAPACKE_spoequ( int matrix_layout, lapack_int n, const float* a,
                           lapack_int lda, float* s, float* scond,
                           float* amax );
lapack_int LAPACKE_dpoequ( int matrix_layout, lapack_int n, const double* a,
                           lapack_int lda, double* s, double* scond,
                           double* amax );
lapack_int LAPACKE_cpoequ( int matrix_layout, lapack_int n,
                           const lapack_complex_float* a, lapack_int lda,
                           float* s, float* scond, float* amax );
lapack_int LAPACKE_zpoequ( int matrix_layout, lapack_int n,
                           const lapack_complex_double* a, lapack_int lda,
                           double* s, double* scond, double* amax );

lapack_int LAPACKE_spoequb( int matrix_layout, lapack_int n, const float* a,
                            lapack_int lda, float* s, float* scond,
                            float* amax );
lapack_int LAPACKE_dpoequb( int matrix_layout, lapack_int n, const double* a,
                            lapack_int lda, double* s, double* scond,
                            double* amax );
lapack_int LAPACKE_cpoequb( int matrix_layout, lapack_int n,
                            const lapack_complex_float* a, lapack_int lda,
                            float* s, float* scond, float* amax );
lapack_int LAPACKE_zpoequb( int matrix_layout, lapack_int n,
                            const lapack_complex_double* a, lapack_int lda,
                            double* s, double* scond, double* amax );

lapack_int LAPACKE_sporfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const float* a, lapack_int lda,
                           const float* af, lapack_int ldaf, const float* b,
                           lapack_int ldb, float* x, lapack_int ldx,
                           float* ferr, float* berr );
lapack_int LAPACKE_dporfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const double* a, lapack_int lda,
                           const double* af, lapack_int ldaf, const double* b,
                           lapack_int ldb, double* x, lapack_int ldx,
                           double* ferr, double* berr );
lapack_int LAPACKE_cporfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* a,
                           lapack_int lda, const lapack_complex_float* af,
                           lapack_int ldaf, const lapack_complex_float* b,
                           lapack_int ldb, lapack_complex_float* x,
                           lapack_int ldx, float* ferr, float* berr );
lapack_int LAPACKE_zporfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* a,
                           lapack_int lda, const lapack_complex_double* af,
                           lapack_int ldaf, const lapack_complex_double* b,
                           lapack_int ldb, lapack_complex_double* x,
                           lapack_int ldx, double* ferr, double* berr );

lapack_int LAPACKE_sporfsx( int matrix_layout, char uplo, char equed,
                            lapack_int n, lapack_int nrhs, const float* a,
                            lapack_int lda, const float* af, lapack_int ldaf,
                            const float* s, const float* b, lapack_int ldb,
                            float* x, lapack_int ldx, float* rcond, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_dporfsx( int matrix_layout, char uplo, char equed,
                            lapack_int n, lapack_int nrhs, const double* a,
                            lapack_int lda, const double* af, lapack_int ldaf,
                            const double* s, const double* b, lapack_int ldb,
                            double* x, lapack_int ldx, double* rcond,
                            double* berr, lapack_int n_err_bnds,
                            double* err_bnds_norm, double* err_bnds_comp,
                            lapack_int nparams, double* params );
lapack_int LAPACKE_cporfsx( int matrix_layout, char uplo, char equed,
                            lapack_int n, lapack_int nrhs,
                            const lapack_complex_float* a, lapack_int lda,
                            const lapack_complex_float* af, lapack_int ldaf,
                            const float* s, const lapack_complex_float* b,
                            lapack_int ldb, lapack_complex_float* x,
                            lapack_int ldx, float* rcond, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_zporfsx( int matrix_layout, char uplo, char equed,
                            lapack_int n, lapack_int nrhs,
                            const lapack_complex_double* a, lapack_int lda,
                            const lapack_complex_double* af, lapack_int ldaf,
                            const double* s, const lapack_complex_double* b,
                            lapack_int ldb, lapack_complex_double* x,
                            lapack_int ldx, double* rcond, double* berr,
                            lapack_int n_err_bnds, double* err_bnds_norm,
                            double* err_bnds_comp, lapack_int nparams,
                            double* params );

lapack_int LAPACKE_sposv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, float* a, lapack_int lda, float* b,
                          lapack_int ldb );
lapack_int LAPACKE_dposv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, double* a, lapack_int lda, double* b,
                          lapack_int ldb );
lapack_int LAPACKE_cposv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_float* a,
                          lapack_int lda, lapack_complex_float* b,
                          lapack_int ldb );
lapack_int LAPACKE_zposv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_double* a,
                          lapack_int lda, lapack_complex_double* b,
                          lapack_int ldb );
lapack_int LAPACKE_dsposv( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, double* a, lapack_int lda,
                           double* b, lapack_int ldb, double* x, lapack_int ldx,
                           lapack_int* iter );
lapack_int LAPACKE_zcposv( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* b,
                           lapack_int ldb, lapack_complex_double* x,
                           lapack_int ldx, lapack_int* iter );

lapack_int LAPACKE_sposvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, float* a, lapack_int lda, float* af,
                           lapack_int ldaf, char* equed, float* s, float* b,
                           lapack_int ldb, float* x, lapack_int ldx,
                           float* rcond, float* ferr, float* berr );
lapack_int LAPACKE_dposvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, double* a, lapack_int lda,
                           double* af, lapack_int ldaf, char* equed, double* s,
                           double* b, lapack_int ldb, double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr );
lapack_int LAPACKE_cposvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* af,
                           lapack_int ldaf, char* equed, float* s,
                           lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx,
                           float* rcond, float* ferr, float* berr );
lapack_int LAPACKE_zposvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* af,
                           lapack_int ldaf, char* equed, double* s,
                           lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr );

lapack_int LAPACKE_sposvxx( int matrix_layout, char fact, char uplo,
                            lapack_int n, lapack_int nrhs, float* a,
                            lapack_int lda, float* af, lapack_int ldaf,
                            char* equed, float* s, float* b, lapack_int ldb,
                            float* x, lapack_int ldx, float* rcond,
                            float* rpvgrw, float* berr, lapack_int n_err_bnds,
                            float* err_bnds_norm, float* err_bnds_comp,
                            lapack_int nparams, float* params );
lapack_int LAPACKE_dposvxx( int matrix_layout, char fact, char uplo,
                            lapack_int n, lapack_int nrhs, double* a,
                            lapack_int lda, double* af, lapack_int ldaf,
                            char* equed, double* s, double* b, lapack_int ldb,
                            double* x, lapack_int ldx, double* rcond,
                            double* rpvgrw, double* berr, lapack_int n_err_bnds,
                            double* err_bnds_norm, double* err_bnds_comp,
                            lapack_int nparams, double* params );
lapack_int LAPACKE_cposvxx( int matrix_layout, char fact, char uplo,
                            lapack_int n, lapack_int nrhs,
                            lapack_complex_float* a, lapack_int lda,
                            lapack_complex_float* af, lapack_int ldaf,
                            char* equed, float* s, lapack_complex_float* b,
                            lapack_int ldb, lapack_complex_float* x,
                            lapack_int ldx, float* rcond, float* rpvgrw,
                            float* berr, lapack_int n_err_bnds,
                            float* err_bnds_norm, float* err_bnds_comp,
                            lapack_int nparams, float* params );
lapack_int LAPACKE_zposvxx( int matrix_layout, char fact, char uplo,
                            lapack_int n, lapack_int nrhs,
                            lapack_complex_double* a, lapack_int lda,
                            lapack_complex_double* af, lapack_int ldaf,
                            char* equed, double* s, lapack_complex_double* b,
                            lapack_int ldb, lapack_complex_double* x,
                            lapack_int ldx, double* rcond, double* rpvgrw,
                            double* berr, lapack_int n_err_bnds,
                            double* err_bnds_norm, double* err_bnds_comp,
                            lapack_int nparams, double* params );

lapack_int LAPACKE_spotrf2( int matrix_layout, char uplo, lapack_int n, float* a,
                           lapack_int lda );
lapack_int LAPACKE_dpotrf2( int matrix_layout, char uplo, lapack_int n, double* a,
                           lapack_int lda );
lapack_int LAPACKE_cpotrf2( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda );
lapack_int LAPACKE_zpotrf2( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda );

lapack_int LAPACKE_spotrf( int matrix_layout, char uplo, lapack_int n, float* a,
                           lapack_int lda );
lapack_int LAPACKE_dpotrf( int matrix_layout, char uplo, lapack_int n, double* a,
                           lapack_int lda );
lapack_int LAPACKE_cpotrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda );
lapack_int LAPACKE_zpotrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda );

lapack_int LAPACKE_spotri( int matrix_layout, char uplo, lapack_int n, float* a,
                           lapack_int lda );
lapack_int LAPACKE_dpotri( int matrix_layout, char uplo, lapack_int n, double* a,
                           lapack_int lda );
lapack_int LAPACKE_cpotri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda );
lapack_int LAPACKE_zpotri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda );

lapack_int LAPACKE_spotrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const float* a, lapack_int lda,
                           float* b, lapack_int ldb );
lapack_int LAPACKE_dpotrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const double* a, lapack_int lda,
                           double* b, lapack_int ldb );
lapack_int LAPACKE_cpotrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* b,
                           lapack_int ldb );
lapack_int LAPACKE_zpotrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* b,
                           lapack_int ldb );

lapack_int LAPACKE_sppcon( int matrix_layout, char uplo, lapack_int n,
                           const float* ap, float anorm, float* rcond );
lapack_int LAPACKE_dppcon( int matrix_layout, char uplo, lapack_int n,
                           const double* ap, double anorm, double* rcond );
lapack_int LAPACKE_cppcon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_float* ap, float anorm,
                           float* rcond );
lapack_int LAPACKE_zppcon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_double* ap, double anorm,
                           double* rcond );

lapack_int LAPACKE_sppequ( int matrix_layout, char uplo, lapack_int n,
                           const float* ap, float* s, float* scond,
                           float* amax );
lapack_int LAPACKE_dppequ( int matrix_layout, char uplo, lapack_int n,
                           const double* ap, double* s, double* scond,
                           double* amax );
lapack_int LAPACKE_cppequ( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_float* ap, float* s,
                           float* scond, float* amax );
lapack_int LAPACKE_zppequ( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_double* ap, double* s,
                           double* scond, double* amax );

lapack_int LAPACKE_spprfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const float* ap, const float* afp,
                           const float* b, lapack_int ldb, float* x,
                           lapack_int ldx, float* ferr, float* berr );
lapack_int LAPACKE_dpprfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const double* ap, const double* afp,
                           const double* b, lapack_int ldb, double* x,
                           lapack_int ldx, double* ferr, double* berr );
lapack_int LAPACKE_cpprfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* ap,
                           const lapack_complex_float* afp,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx, float* ferr,
                           float* berr );
lapack_int LAPACKE_zpprfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* ap,
                           const lapack_complex_double* afp,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* ferr, double* berr );

lapack_int LAPACKE_sppsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, float* ap, float* b,
                          lapack_int ldb );
lapack_int LAPACKE_dppsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, double* ap, double* b,
                          lapack_int ldb );
lapack_int LAPACKE_cppsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_float* ap,
                          lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zppsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_double* ap,
                          lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_sppsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, float* ap, float* afp, char* equed,
                           float* s, float* b, lapack_int ldb, float* x,
                           lapack_int ldx, float* rcond, float* ferr,
                           float* berr );
lapack_int LAPACKE_dppsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, double* ap, double* afp,
                           char* equed, double* s, double* b, lapack_int ldb,
                           double* x, lapack_int ldx, double* rcond,
                           double* ferr, double* berr );
lapack_int LAPACKE_cppsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, lapack_complex_float* ap,
                           lapack_complex_float* afp, char* equed, float* s,
                           lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx,
                           float* rcond, float* ferr, float* berr );
lapack_int LAPACKE_zppsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, lapack_complex_double* ap,
                           lapack_complex_double* afp, char* equed, double* s,
                           lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr );

lapack_int LAPACKE_spptrf( int matrix_layout, char uplo, lapack_int n,
                           float* ap );
lapack_int LAPACKE_dpptrf( int matrix_layout, char uplo, lapack_int n,
                           double* ap );
lapack_int LAPACKE_cpptrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* ap );
lapack_int LAPACKE_zpptrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* ap );

lapack_int LAPACKE_spptri( int matrix_layout, char uplo, lapack_int n,
                           float* ap );
lapack_int LAPACKE_dpptri( int matrix_layout, char uplo, lapack_int n,
                           double* ap );
lapack_int LAPACKE_cpptri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* ap );
lapack_int LAPACKE_zpptri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* ap );

lapack_int LAPACKE_spptrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const float* ap, float* b,
                           lapack_int ldb );
lapack_int LAPACKE_dpptrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const double* ap, double* b,
                           lapack_int ldb );
lapack_int LAPACKE_cpptrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* ap,
                           lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zpptrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* ap,
                           lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_spstrf( int matrix_layout, char uplo, lapack_int n, float* a,
                           lapack_int lda, lapack_int* piv, lapack_int* rank,
                           float tol );
lapack_int LAPACKE_dpstrf( int matrix_layout, char uplo, lapack_int n, double* a,
                           lapack_int lda, lapack_int* piv, lapack_int* rank,
                           double tol );
lapack_int LAPACKE_cpstrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int* piv, lapack_int* rank, float tol );
lapack_int LAPACKE_zpstrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* piv, lapack_int* rank, double tol );

lapack_int LAPACKE_sptcon( lapack_int n, const float* d, const float* e,
                           float anorm, float* rcond );
lapack_int LAPACKE_dptcon( lapack_int n, const double* d, const double* e,
                           double anorm, double* rcond );
lapack_int LAPACKE_cptcon( lapack_int n, const float* d,
                           const lapack_complex_float* e, float anorm,
                           float* rcond );
lapack_int LAPACKE_zptcon( lapack_int n, const double* d,
                           const lapack_complex_double* e, double anorm,
                           double* rcond );

lapack_int LAPACKE_spteqr( int matrix_layout, char compz, lapack_int n, float* d,
                           float* e, float* z, lapack_int ldz );
lapack_int LAPACKE_dpteqr( int matrix_layout, char compz, lapack_int n,
                           double* d, double* e, double* z, lapack_int ldz );
lapack_int LAPACKE_cpteqr( int matrix_layout, char compz, lapack_int n, float* d,
                           float* e, lapack_complex_float* z, lapack_int ldz );
lapack_int LAPACKE_zpteqr( int matrix_layout, char compz, lapack_int n,
                           double* d, double* e, lapack_complex_double* z,
                           lapack_int ldz );

lapack_int LAPACKE_sptrfs( int matrix_layout, lapack_int n, lapack_int nrhs,
                           const float* d, const float* e, const float* df,
                           const float* ef, const float* b, lapack_int ldb,
                           float* x, lapack_int ldx, float* ferr, float* berr );
lapack_int LAPACKE_dptrfs( int matrix_layout, lapack_int n, lapack_int nrhs,
                           const double* d, const double* e, const double* df,
                           const double* ef, const double* b, lapack_int ldb,
                           double* x, lapack_int ldx, double* ferr,
                           double* berr );
lapack_int LAPACKE_cptrfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const float* d,
                           const lapack_complex_float* e, const float* df,
                           const lapack_complex_float* ef,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx, float* ferr,
                           float* berr );
lapack_int LAPACKE_zptrfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const double* d,
                           const lapack_complex_double* e, const double* df,
                           const lapack_complex_double* ef,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* ferr, double* berr );

lapack_int LAPACKE_sptsv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          float* d, float* e, float* b, lapack_int ldb );
lapack_int LAPACKE_dptsv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          double* d, double* e, double* b, lapack_int ldb );
lapack_int LAPACKE_cptsv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          float* d, lapack_complex_float* e,
                          lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zptsv( int matrix_layout, lapack_int n, lapack_int nrhs,
                          double* d, lapack_complex_double* e,
                          lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_sptsvx( int matrix_layout, char fact, lapack_int n,
                           lapack_int nrhs, const float* d, const float* e,
                           float* df, float* ef, const float* b, lapack_int ldb,
                           float* x, lapack_int ldx, float* rcond, float* ferr,
                           float* berr );
lapack_int LAPACKE_dptsvx( int matrix_layout, char fact, lapack_int n,
                           lapack_int nrhs, const double* d, const double* e,
                           double* df, double* ef, const double* b,
                           lapack_int ldb, double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr );
lapack_int LAPACKE_cptsvx( int matrix_layout, char fact, lapack_int n,
                           lapack_int nrhs, const float* d,
                           const lapack_complex_float* e, float* df,
                           lapack_complex_float* ef,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx,
                           float* rcond, float* ferr, float* berr );
lapack_int LAPACKE_zptsvx( int matrix_layout, char fact, lapack_int n,
                           lapack_int nrhs, const double* d,
                           const lapack_complex_double* e, double* df,
                           lapack_complex_double* ef,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr );

lapack_int LAPACKE_spttrf( lapack_int n, float* d, float* e );
lapack_int LAPACKE_dpttrf( lapack_int n, double* d, double* e );
lapack_int LAPACKE_cpttrf( lapack_int n, float* d, lapack_complex_float* e );
lapack_int LAPACKE_zpttrf( lapack_int n, double* d, lapack_complex_double* e );

lapack_int LAPACKE_spttrs( int matrix_layout, lapack_int n, lapack_int nrhs,
                           const float* d, const float* e, float* b,
                           lapack_int ldb );
lapack_int LAPACKE_dpttrs( int matrix_layout, lapack_int n, lapack_int nrhs,
                           const double* d, const double* e, double* b,
                           lapack_int ldb );
lapack_int LAPACKE_cpttrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const float* d,
                           const lapack_complex_float* e,
                           lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zpttrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const double* d,
                           const lapack_complex_double* e,
                           lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_ssbev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_int kd, float* ab, lapack_int ldab, float* w,
                          float* z, lapack_int ldz );
lapack_int LAPACKE_dsbev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_int kd, double* ab, lapack_int ldab, double* w,
                          double* z, lapack_int ldz );

lapack_int LAPACKE_ssbevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_int kd, float* ab, lapack_int ldab, float* w,
                           float* z, lapack_int ldz );
lapack_int LAPACKE_dsbevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_int kd, double* ab, lapack_int ldab,
                           double* w, double* z, lapack_int ldz );

lapack_int LAPACKE_ssbevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_int kd, float* ab,
                           lapack_int ldab, float* q, lapack_int ldq, float vl,
                           float vu, lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, float* z, lapack_int ldz,
                           lapack_int* ifail );
lapack_int LAPACKE_dsbevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_int kd, double* ab,
                           lapack_int ldab, double* q, lapack_int ldq,
                           double vl, double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w, double* z,
                           lapack_int ldz, lapack_int* ifail );

lapack_int LAPACKE_ssbgst( int matrix_layout, char vect, char uplo, lapack_int n,
                           lapack_int ka, lapack_int kb, float* ab,
                           lapack_int ldab, const float* bb, lapack_int ldbb,
                           float* x, lapack_int ldx );
lapack_int LAPACKE_dsbgst( int matrix_layout, char vect, char uplo, lapack_int n,
                           lapack_int ka, lapack_int kb, double* ab,
                           lapack_int ldab, const double* bb, lapack_int ldbb,
                           double* x, lapack_int ldx );

lapack_int LAPACKE_ssbgv( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_int ka, lapack_int kb, float* ab,
                          lapack_int ldab, float* bb, lapack_int ldbb, float* w,
                          float* z, lapack_int ldz );
lapack_int LAPACKE_dsbgv( int matrix_layout, char jobz, char uplo, lapack_int n,
                          lapack_int ka, lapack_int kb, double* ab,
                          lapack_int ldab, double* bb, lapack_int ldbb,
                          double* w, double* z, lapack_int ldz );

lapack_int LAPACKE_ssbgvd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_int ka, lapack_int kb, float* ab,
                           lapack_int ldab, float* bb, lapack_int ldbb,
                           float* w, float* z, lapack_int ldz );
lapack_int LAPACKE_dsbgvd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           lapack_int ka, lapack_int kb, double* ab,
                           lapack_int ldab, double* bb, lapack_int ldbb,
                           double* w, double* z, lapack_int ldz );

lapack_int LAPACKE_ssbgvx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_int ka, lapack_int kb,
                           float* ab, lapack_int ldab, float* bb,
                           lapack_int ldbb, float* q, lapack_int ldq, float vl,
                           float vu, lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, float* z, lapack_int ldz,
                           lapack_int* ifail );
lapack_int LAPACKE_dsbgvx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, lapack_int ka, lapack_int kb,
                           double* ab, lapack_int ldab, double* bb,
                           lapack_int ldbb, double* q, lapack_int ldq,
                           double vl, double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w, double* z,
                           lapack_int ldz, lapack_int* ifail );

lapack_int LAPACKE_ssbtrd( int matrix_layout, char vect, char uplo, lapack_int n,
                           lapack_int kd, float* ab, lapack_int ldab, float* d,
                           float* e, float* q, lapack_int ldq );
lapack_int LAPACKE_dsbtrd( int matrix_layout, char vect, char uplo, lapack_int n,
                           lapack_int kd, double* ab, lapack_int ldab,
                           double* d, double* e, double* q, lapack_int ldq );

lapack_int LAPACKE_ssfrk( int matrix_layout, char transr, char uplo, char trans,
                          lapack_int n, lapack_int k, float alpha,
                          const float* a, lapack_int lda, float beta,
                          float* c );
lapack_int LAPACKE_dsfrk( int matrix_layout, char transr, char uplo, char trans,
                          lapack_int n, lapack_int k, double alpha,
                          const double* a, lapack_int lda, double beta,
                          double* c );

lapack_int LAPACKE_sspcon( int matrix_layout, char uplo, lapack_int n,
                           const float* ap, const lapack_int* ipiv, float anorm,
                           float* rcond );
lapack_int LAPACKE_dspcon( int matrix_layout, char uplo, lapack_int n,
                           const double* ap, const lapack_int* ipiv,
                           double anorm, double* rcond );
lapack_int LAPACKE_cspcon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_float* ap,
                           const lapack_int* ipiv, float anorm, float* rcond );
lapack_int LAPACKE_zspcon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_double* ap,
                           const lapack_int* ipiv, double anorm,
                           double* rcond );

lapack_int LAPACKE_sspev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          float* ap, float* w, float* z, lapack_int ldz );
lapack_int LAPACKE_dspev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          double* ap, double* w, double* z, lapack_int ldz );

lapack_int LAPACKE_sspevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           float* ap, float* w, float* z, lapack_int ldz );
lapack_int LAPACKE_dspevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           double* ap, double* w, double* z, lapack_int ldz );

lapack_int LAPACKE_sspevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, float* ap, float vl, float vu,
                           lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, float* z, lapack_int ldz,
                           lapack_int* ifail );
lapack_int LAPACKE_dspevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, double* ap, double vl, double vu,
                           lapack_int il, lapack_int iu, double abstol,
                           lapack_int* m, double* w, double* z, lapack_int ldz,
                           lapack_int* ifail );

lapack_int LAPACKE_sspgst( int matrix_layout, lapack_int itype, char uplo,
                           lapack_int n, float* ap, const float* bp );
lapack_int LAPACKE_dspgst( int matrix_layout, lapack_int itype, char uplo,
                           lapack_int n, double* ap, const double* bp );

lapack_int LAPACKE_sspgv( int matrix_layout, lapack_int itype, char jobz,
                          char uplo, lapack_int n, float* ap, float* bp,
                          float* w, float* z, lapack_int ldz );
lapack_int LAPACKE_dspgv( int matrix_layout, lapack_int itype, char jobz,
                          char uplo, lapack_int n, double* ap, double* bp,
                          double* w, double* z, lapack_int ldz );

lapack_int LAPACKE_sspgvd( int matrix_layout, lapack_int itype, char jobz,
                           char uplo, lapack_int n, float* ap, float* bp,
                           float* w, float* z, lapack_int ldz );
lapack_int LAPACKE_dspgvd( int matrix_layout, lapack_int itype, char jobz,
                           char uplo, lapack_int n, double* ap, double* bp,
                           double* w, double* z, lapack_int ldz );

lapack_int LAPACKE_sspgvx( int matrix_layout, lapack_int itype, char jobz,
                           char range, char uplo, lapack_int n, float* ap,
                           float* bp, float vl, float vu, lapack_int il,
                           lapack_int iu, float abstol, lapack_int* m, float* w,
                           float* z, lapack_int ldz, lapack_int* ifail );
lapack_int LAPACKE_dspgvx( int matrix_layout, lapack_int itype, char jobz,
                           char range, char uplo, lapack_int n, double* ap,
                           double* bp, double vl, double vu, lapack_int il,
                           lapack_int iu, double abstol, lapack_int* m,
                           double* w, double* z, lapack_int ldz,
                           lapack_int* ifail );

lapack_int LAPACKE_ssprfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const float* ap, const float* afp,
                           const lapack_int* ipiv, const float* b,
                           lapack_int ldb, float* x, lapack_int ldx,
                           float* ferr, float* berr );
lapack_int LAPACKE_dsprfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const double* ap, const double* afp,
                           const lapack_int* ipiv, const double* b,
                           lapack_int ldb, double* x, lapack_int ldx,
                           double* ferr, double* berr );
lapack_int LAPACKE_csprfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* ap,
                           const lapack_complex_float* afp,
                           const lapack_int* ipiv,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx, float* ferr,
                           float* berr );
lapack_int LAPACKE_zsprfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* ap,
                           const lapack_complex_double* afp,
                           const lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* ferr, double* berr );

lapack_int LAPACKE_sspsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, float* ap, lapack_int* ipiv,
                          float* b, lapack_int ldb );
lapack_int LAPACKE_dspsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, double* ap, lapack_int* ipiv,
                          double* b, lapack_int ldb );
lapack_int LAPACKE_cspsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_float* ap,
                          lapack_int* ipiv, lapack_complex_float* b,
                          lapack_int ldb );
lapack_int LAPACKE_zspsv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_double* ap,
                          lapack_int* ipiv, lapack_complex_double* b,
                          lapack_int ldb );

lapack_int LAPACKE_sspsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const float* ap, float* afp,
                           lapack_int* ipiv, const float* b, lapack_int ldb,
                           float* x, lapack_int ldx, float* rcond, float* ferr,
                           float* berr );
lapack_int LAPACKE_dspsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const double* ap, double* afp,
                           lapack_int* ipiv, const double* b, lapack_int ldb,
                           double* x, lapack_int ldx, double* rcond,
                           double* ferr, double* berr );
lapack_int LAPACKE_cspsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* ap,
                           lapack_complex_float* afp, lapack_int* ipiv,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx,
                           float* rcond, float* ferr, float* berr );
lapack_int LAPACKE_zspsvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* ap,
                           lapack_complex_double* afp, lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr );

lapack_int LAPACKE_ssptrd( int matrix_layout, char uplo, lapack_int n, float* ap,
                           float* d, float* e, float* tau );
lapack_int LAPACKE_dsptrd( int matrix_layout, char uplo, lapack_int n,
                           double* ap, double* d, double* e, double* tau );

lapack_int LAPACKE_ssptrf( int matrix_layout, char uplo, lapack_int n, float* ap,
                           lapack_int* ipiv );
lapack_int LAPACKE_dsptrf( int matrix_layout, char uplo, lapack_int n,
                           double* ap, lapack_int* ipiv );
lapack_int LAPACKE_csptrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* ap, lapack_int* ipiv );
lapack_int LAPACKE_zsptrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* ap, lapack_int* ipiv );

lapack_int LAPACKE_ssptri( int matrix_layout, char uplo, lapack_int n, float* ap,
                           const lapack_int* ipiv );
lapack_int LAPACKE_dsptri( int matrix_layout, char uplo, lapack_int n,
                           double* ap, const lapack_int* ipiv );
lapack_int LAPACKE_csptri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* ap, const lapack_int* ipiv );
lapack_int LAPACKE_zsptri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* ap, const lapack_int* ipiv );

lapack_int LAPACKE_ssptrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const float* ap,
                           const lapack_int* ipiv, float* b, lapack_int ldb );
lapack_int LAPACKE_dsptrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const double* ap,
                           const lapack_int* ipiv, double* b, lapack_int ldb );
lapack_int LAPACKE_csptrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* ap,
                           const lapack_int* ipiv, lapack_complex_float* b,
                           lapack_int ldb );
lapack_int LAPACKE_zsptrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* ap,
                           const lapack_int* ipiv, lapack_complex_double* b,
                           lapack_int ldb );

lapack_int LAPACKE_sstebz( char range, char order, lapack_int n, float vl,
                           float vu, lapack_int il, lapack_int iu, float abstol,
                           const float* d, const float* e, lapack_int* m,
                           lapack_int* nsplit, float* w, lapack_int* iblock,
                           lapack_int* isplit );
lapack_int LAPACKE_dstebz( char range, char order, lapack_int n, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, const double* d, const double* e,
                           lapack_int* m, lapack_int* nsplit, double* w,
                           lapack_int* iblock, lapack_int* isplit );

lapack_int LAPACKE_sstedc( int matrix_layout, char compz, lapack_int n, float* d,
                           float* e, float* z, lapack_int ldz );
lapack_int LAPACKE_dstedc( int matrix_layout, char compz, lapack_int n,
                           double* d, double* e, double* z, lapack_int ldz );
lapack_int LAPACKE_cstedc( int matrix_layout, char compz, lapack_int n, float* d,
                           float* e, lapack_complex_float* z, lapack_int ldz );
lapack_int LAPACKE_zstedc( int matrix_layout, char compz, lapack_int n,
                           double* d, double* e, lapack_complex_double* z,
                           lapack_int ldz );

lapack_int LAPACKE_sstegr( int matrix_layout, char jobz, char range,
                           lapack_int n, float* d, float* e, float vl, float vu,
                           lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, float* z, lapack_int ldz,
                           lapack_int* isuppz );
lapack_int LAPACKE_dstegr( int matrix_layout, char jobz, char range,
                           lapack_int n, double* d, double* e, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w, double* z,
                           lapack_int ldz, lapack_int* isuppz );
lapack_int LAPACKE_cstegr( int matrix_layout, char jobz, char range,
                           lapack_int n, float* d, float* e, float vl, float vu,
                           lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, lapack_complex_float* z,
                           lapack_int ldz, lapack_int* isuppz );
lapack_int LAPACKE_zstegr( int matrix_layout, char jobz, char range,
                           lapack_int n, double* d, double* e, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w,
                           lapack_complex_double* z, lapack_int ldz,
                           lapack_int* isuppz );

lapack_int LAPACKE_sstein( int matrix_layout, lapack_int n, const float* d,
                           const float* e, lapack_int m, const float* w,
                           const lapack_int* iblock, const lapack_int* isplit,
                           float* z, lapack_int ldz, lapack_int* ifailv );
lapack_int LAPACKE_dstein( int matrix_layout, lapack_int n, const double* d,
                           const double* e, lapack_int m, const double* w,
                           const lapack_int* iblock, const lapack_int* isplit,
                           double* z, lapack_int ldz, lapack_int* ifailv );
lapack_int LAPACKE_cstein( int matrix_layout, lapack_int n, const float* d,
                           const float* e, lapack_int m, const float* w,
                           const lapack_int* iblock, const lapack_int* isplit,
                           lapack_complex_float* z, lapack_int ldz,
                           lapack_int* ifailv );
lapack_int LAPACKE_zstein( int matrix_layout, lapack_int n, const double* d,
                           const double* e, lapack_int m, const double* w,
                           const lapack_int* iblock, const lapack_int* isplit,
                           lapack_complex_double* z, lapack_int ldz,
                           lapack_int* ifailv );

lapack_int LAPACKE_sstemr( int matrix_layout, char jobz, char range,
                           lapack_int n, float* d, float* e, float vl, float vu,
                           lapack_int il, lapack_int iu, lapack_int* m,
                           float* w, float* z, lapack_int ldz, lapack_int nzc,
                           lapack_int* isuppz, lapack_logical* tryrac );
lapack_int LAPACKE_dstemr( int matrix_layout, char jobz, char range,
                           lapack_int n, double* d, double* e, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           lapack_int* m, double* w, double* z, lapack_int ldz,
                           lapack_int nzc, lapack_int* isuppz,
                           lapack_logical* tryrac );
lapack_int LAPACKE_cstemr( int matrix_layout, char jobz, char range,
                           lapack_int n, float* d, float* e, float vl, float vu,
                           lapack_int il, lapack_int iu, lapack_int* m,
                           float* w, lapack_complex_float* z, lapack_int ldz,
                           lapack_int nzc, lapack_int* isuppz,
                           lapack_logical* tryrac );
lapack_int LAPACKE_zstemr( int matrix_layout, char jobz, char range,
                           lapack_int n, double* d, double* e, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           lapack_int* m, double* w, lapack_complex_double* z,
                           lapack_int ldz, lapack_int nzc, lapack_int* isuppz,
                           lapack_logical* tryrac );

lapack_int LAPACKE_ssteqr( int matrix_layout, char compz, lapack_int n, float* d,
                           float* e, float* z, lapack_int ldz );
lapack_int LAPACKE_dsteqr( int matrix_layout, char compz, lapack_int n,
                           double* d, double* e, double* z, lapack_int ldz );
lapack_int LAPACKE_csteqr( int matrix_layout, char compz, lapack_int n, float* d,
                           float* e, lapack_complex_float* z, lapack_int ldz );
lapack_int LAPACKE_zsteqr( int matrix_layout, char compz, lapack_int n,
                           double* d, double* e, lapack_complex_double* z,
                           lapack_int ldz );

lapack_int LAPACKE_ssterf( lapack_int n, float* d, float* e );
lapack_int LAPACKE_dsterf( lapack_int n, double* d, double* e );

lapack_int LAPACKE_sstev( int matrix_layout, char jobz, lapack_int n, float* d,
                          float* e, float* z, lapack_int ldz );
lapack_int LAPACKE_dstev( int matrix_layout, char jobz, lapack_int n, double* d,
                          double* e, double* z, lapack_int ldz );

lapack_int LAPACKE_sstevd( int matrix_layout, char jobz, lapack_int n, float* d,
                           float* e, float* z, lapack_int ldz );
lapack_int LAPACKE_dstevd( int matrix_layout, char jobz, lapack_int n, double* d,
                           double* e, double* z, lapack_int ldz );

lapack_int LAPACKE_sstevr( int matrix_layout, char jobz, char range,
                           lapack_int n, float* d, float* e, float vl, float vu,
                           lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, float* z, lapack_int ldz,
                           lapack_int* isuppz );
lapack_int LAPACKE_dstevr( int matrix_layout, char jobz, char range,
                           lapack_int n, double* d, double* e, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w, double* z,
                           lapack_int ldz, lapack_int* isuppz );

lapack_int LAPACKE_sstevx( int matrix_layout, char jobz, char range,
                           lapack_int n, float* d, float* e, float vl, float vu,
                           lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, float* z, lapack_int ldz,
                           lapack_int* ifail );
lapack_int LAPACKE_dstevx( int matrix_layout, char jobz, char range,
                           lapack_int n, double* d, double* e, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w, double* z,
                           lapack_int ldz, lapack_int* ifail );

lapack_int LAPACKE_ssycon( int matrix_layout, char uplo, lapack_int n,
                           const float* a, lapack_int lda,
                           const lapack_int* ipiv, float anorm, float* rcond );
lapack_int LAPACKE_dsycon( int matrix_layout, char uplo, lapack_int n,
                           const double* a, lapack_int lda,
                           const lapack_int* ipiv, double anorm,
                           double* rcond );
lapack_int LAPACKE_csycon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_float* a, lapack_int lda,
                           const lapack_int* ipiv, float anorm, float* rcond );
lapack_int LAPACKE_zsycon( int matrix_layout, char uplo, lapack_int n,
                           const lapack_complex_double* a, lapack_int lda,
                           const lapack_int* ipiv, double anorm,
                           double* rcond );

lapack_int LAPACKE_ssyequb( int matrix_layout, char uplo, lapack_int n,
                            const float* a, lapack_int lda, float* s,
                            float* scond, float* amax );
lapack_int LAPACKE_dsyequb( int matrix_layout, char uplo, lapack_int n,
                            const double* a, lapack_int lda, double* s,
                            double* scond, double* amax );
lapack_int LAPACKE_csyequb( int matrix_layout, char uplo, lapack_int n,
                            const lapack_complex_float* a, lapack_int lda,
                            float* s, float* scond, float* amax );
lapack_int LAPACKE_zsyequb( int matrix_layout, char uplo, lapack_int n,
                            const lapack_complex_double* a, lapack_int lda,
                            double* s, double* scond, double* amax );

lapack_int LAPACKE_ssyev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          float* a, lapack_int lda, float* w );
lapack_int LAPACKE_dsyev( int matrix_layout, char jobz, char uplo, lapack_int n,
                          double* a, lapack_int lda, double* w );

lapack_int LAPACKE_ssyevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           float* a, lapack_int lda, float* w );
lapack_int LAPACKE_dsyevd( int matrix_layout, char jobz, char uplo, lapack_int n,
                           double* a, lapack_int lda, double* w );

lapack_int LAPACKE_ssyevr( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, float* a, lapack_int lda, float vl,
                           float vu, lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, float* z, lapack_int ldz,
                           lapack_int* isuppz );
lapack_int LAPACKE_dsyevr( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, double* a, lapack_int lda, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w, double* z,
                           lapack_int ldz, lapack_int* isuppz );

lapack_int LAPACKE_ssyevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, float* a, lapack_int lda, float vl,
                           float vu, lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, float* z, lapack_int ldz,
                           lapack_int* ifail );
lapack_int LAPACKE_dsyevx( int matrix_layout, char jobz, char range, char uplo,
                           lapack_int n, double* a, lapack_int lda, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w, double* z,
                           lapack_int ldz, lapack_int* ifail );

lapack_int LAPACKE_ssygst( int matrix_layout, lapack_int itype, char uplo,
                           lapack_int n, float* a, lapack_int lda,
                           const float* b, lapack_int ldb );
lapack_int LAPACKE_dsygst( int matrix_layout, lapack_int itype, char uplo,
                           lapack_int n, double* a, lapack_int lda,
                           const double* b, lapack_int ldb );

lapack_int LAPACKE_ssygv( int matrix_layout, lapack_int itype, char jobz,
                          char uplo, lapack_int n, float* a, lapack_int lda,
                          float* b, lapack_int ldb, float* w );
lapack_int LAPACKE_dsygv( int matrix_layout, lapack_int itype, char jobz,
                          char uplo, lapack_int n, double* a, lapack_int lda,
                          double* b, lapack_int ldb, double* w );

lapack_int LAPACKE_ssygvd( int matrix_layout, lapack_int itype, char jobz,
                           char uplo, lapack_int n, float* a, lapack_int lda,
                           float* b, lapack_int ldb, float* w );
lapack_int LAPACKE_dsygvd( int matrix_layout, lapack_int itype, char jobz,
                           char uplo, lapack_int n, double* a, lapack_int lda,
                           double* b, lapack_int ldb, double* w );

lapack_int LAPACKE_ssygvx( int matrix_layout, lapack_int itype, char jobz,
                           char range, char uplo, lapack_int n, float* a,
                           lapack_int lda, float* b, lapack_int ldb, float vl,
                           float vu, lapack_int il, lapack_int iu, float abstol,
                           lapack_int* m, float* w, float* z, lapack_int ldz,
                           lapack_int* ifail );
lapack_int LAPACKE_dsygvx( int matrix_layout, lapack_int itype, char jobz,
                           char range, char uplo, lapack_int n, double* a,
                           lapack_int lda, double* b, lapack_int ldb, double vl,
                           double vu, lapack_int il, lapack_int iu,
                           double abstol, lapack_int* m, double* w, double* z,
                           lapack_int ldz, lapack_int* ifail );

lapack_int LAPACKE_ssyrfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const float* a, lapack_int lda,
                           const float* af, lapack_int ldaf,
                           const lapack_int* ipiv, const float* b,
                           lapack_int ldb, float* x, lapack_int ldx,
                           float* ferr, float* berr );
lapack_int LAPACKE_dsyrfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const double* a, lapack_int lda,
                           const double* af, lapack_int ldaf,
                           const lapack_int* ipiv, const double* b,
                           lapack_int ldb, double* x, lapack_int ldx,
                           double* ferr, double* berr );
lapack_int LAPACKE_csyrfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* a,
                           lapack_int lda, const lapack_complex_float* af,
                           lapack_int ldaf, const lapack_int* ipiv,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx, float* ferr,
                           float* berr );
lapack_int LAPACKE_zsyrfs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* a,
                           lapack_int lda, const lapack_complex_double* af,
                           lapack_int ldaf, const lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* ferr, double* berr );

lapack_int LAPACKE_ssyrfsx( int matrix_layout, char uplo, char equed,
                            lapack_int n, lapack_int nrhs, const float* a,
                            lapack_int lda, const float* af, lapack_int ldaf,
                            const lapack_int* ipiv, const float* s,
                            const float* b, lapack_int ldb, float* x,
                            lapack_int ldx, float* rcond, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_dsyrfsx( int matrix_layout, char uplo, char equed,
                            lapack_int n, lapack_int nrhs, const double* a,
                            lapack_int lda, const double* af, lapack_int ldaf,
                            const lapack_int* ipiv, const double* s,
                            const double* b, lapack_int ldb, double* x,
                            lapack_int ldx, double* rcond, double* berr,
                            lapack_int n_err_bnds, double* err_bnds_norm,
                            double* err_bnds_comp, lapack_int nparams,
                            double* params );
lapack_int LAPACKE_csyrfsx( int matrix_layout, char uplo, char equed,
                            lapack_int n, lapack_int nrhs,
                            const lapack_complex_float* a, lapack_int lda,
                            const lapack_complex_float* af, lapack_int ldaf,
                            const lapack_int* ipiv, const float* s,
                            const lapack_complex_float* b, lapack_int ldb,
                            lapack_complex_float* x, lapack_int ldx,
                            float* rcond, float* berr, lapack_int n_err_bnds,
                            float* err_bnds_norm, float* err_bnds_comp,
                            lapack_int nparams, float* params );
lapack_int LAPACKE_zsyrfsx( int matrix_layout, char uplo, char equed,
                            lapack_int n, lapack_int nrhs,
                            const lapack_complex_double* a, lapack_int lda,
                            const lapack_complex_double* af, lapack_int ldaf,
                            const lapack_int* ipiv, const double* s,
                            const lapack_complex_double* b, lapack_int ldb,
                            lapack_complex_double* x, lapack_int ldx,
                            double* rcond, double* berr, lapack_int n_err_bnds,
                            double* err_bnds_norm, double* err_bnds_comp,
                            lapack_int nparams, double* params );

lapack_int LAPACKE_ssysv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, float* a, lapack_int lda,
                          lapack_int* ipiv, float* b, lapack_int ldb );
lapack_int LAPACKE_dsysv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, double* a, lapack_int lda,
                          lapack_int* ipiv, double* b, lapack_int ldb );
lapack_int LAPACKE_csysv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_float* a,
                          lapack_int lda, lapack_int* ipiv,
                          lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zsysv( int matrix_layout, char uplo, lapack_int n,
                          lapack_int nrhs, lapack_complex_double* a,
                          lapack_int lda, lapack_int* ipiv,
                          lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_ssysvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const float* a, lapack_int lda,
                           float* af, lapack_int ldaf, lapack_int* ipiv,
                           const float* b, lapack_int ldb, float* x,
                           lapack_int ldx, float* rcond, float* ferr,
                           float* berr );
lapack_int LAPACKE_dsysvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const double* a, lapack_int lda,
                           double* af, lapack_int ldaf, lapack_int* ipiv,
                           const double* b, lapack_int ldb, double* x,
                           lapack_int ldx, double* rcond, double* ferr,
                           double* berr );
lapack_int LAPACKE_csysvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* a,
                           lapack_int lda, lapack_complex_float* af,
                           lapack_int ldaf, lapack_int* ipiv,
                           const lapack_complex_float* b, lapack_int ldb,
                           lapack_complex_float* x, lapack_int ldx,
                           float* rcond, float* ferr, float* berr );
lapack_int LAPACKE_zsysvx( int matrix_layout, char fact, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* a,
                           lapack_int lda, lapack_complex_double* af,
                           lapack_int ldaf, lapack_int* ipiv,
                           const lapack_complex_double* b, lapack_int ldb,
                           lapack_complex_double* x, lapack_int ldx,
                           double* rcond, double* ferr, double* berr );

lapack_int LAPACKE_ssysvxx( int matrix_layout, char fact, char uplo,
                            lapack_int n, lapack_int nrhs, float* a,
                            lapack_int lda, float* af, lapack_int ldaf,
                            lapack_int* ipiv, char* equed, float* s, float* b,
                            lapack_int ldb, float* x, lapack_int ldx,
                            float* rcond, float* rpvgrw, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_dsysvxx( int matrix_layout, char fact, char uplo,
                            lapack_int n, lapack_int nrhs, double* a,
                            lapack_int lda, double* af, lapack_int ldaf,
                            lapack_int* ipiv, char* equed, double* s, double* b,
                            lapack_int ldb, double* x, lapack_int ldx,
                            double* rcond, double* rpvgrw, double* berr,
                            lapack_int n_err_bnds, double* err_bnds_norm,
                            double* err_bnds_comp, lapack_int nparams,
                            double* params );
lapack_int LAPACKE_csysvxx( int matrix_layout, char fact, char uplo,
                            lapack_int n, lapack_int nrhs,
                            lapack_complex_float* a, lapack_int lda,
                            lapack_complex_float* af, lapack_int ldaf,
                            lapack_int* ipiv, char* equed, float* s,
                            lapack_complex_float* b, lapack_int ldb,
                            lapack_complex_float* x, lapack_int ldx,
                            float* rcond, float* rpvgrw, float* berr,
                            lapack_int n_err_bnds, float* err_bnds_norm,
                            float* err_bnds_comp, lapack_int nparams,
                            float* params );
lapack_int LAPACKE_zsysvxx( int matrix_layout, char fact, char uplo,
                            lapack_int n, lapack_int nrhs,
                            lapack_complex_double* a, lapack_int lda,
                            lapack_complex_double* af, lapack_int ldaf,
                            lapack_int* ipiv, char* equed, double* s,
                            lapack_complex_double* b, lapack_int ldb,
                            lapack_complex_double* x, lapack_int ldx,
                            double* rcond, double* rpvgrw, double* berr,
                            lapack_int n_err_bnds, double* err_bnds_norm,
                            double* err_bnds_comp, lapack_int nparams,
                            double* params );

lapack_int LAPACKE_ssytrd( int matrix_layout, char uplo, lapack_int n, float* a,
                           lapack_int lda, float* d, float* e, float* tau );
lapack_int LAPACKE_dsytrd( int matrix_layout, char uplo, lapack_int n, double* a,
                           lapack_int lda, double* d, double* e, double* tau );

lapack_int LAPACKE_ssytrf( int matrix_layout, char uplo, lapack_int n, float* a,
                           lapack_int lda, lapack_int* ipiv );
lapack_int LAPACKE_dsytrf( int matrix_layout, char uplo, lapack_int n, double* a,
                           lapack_int lda, lapack_int* ipiv );
lapack_int LAPACKE_csytrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           lapack_int* ipiv );
lapack_int LAPACKE_zsytrf( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           lapack_int* ipiv );

lapack_int LAPACKE_ssytri( int matrix_layout, char uplo, lapack_int n, float* a,
                           lapack_int lda, const lapack_int* ipiv );
lapack_int LAPACKE_dsytri( int matrix_layout, char uplo, lapack_int n, double* a,
                           lapack_int lda, const lapack_int* ipiv );
lapack_int LAPACKE_csytri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_float* a, lapack_int lda,
                           const lapack_int* ipiv );
lapack_int LAPACKE_zsytri( int matrix_layout, char uplo, lapack_int n,
                           lapack_complex_double* a, lapack_int lda,
                           const lapack_int* ipiv );

lapack_int LAPACKE_ssytrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const float* a, lapack_int lda,
                           const lapack_int* ipiv, float* b, lapack_int ldb );
lapack_int LAPACKE_dsytrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const double* a, lapack_int lda,
                           const lapack_int* ipiv, double* b, lapack_int ldb );
lapack_int LAPACKE_csytrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_float* a,
                           lapack_int lda, const lapack_int* ipiv,
                           lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_zsytrs( int matrix_layout, char uplo, lapack_int n,
                           lapack_int nrhs, const lapack_complex_double* a,
                           lapack_int lda, const lapack_int* ipiv,
                           lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_stbcon( int matrix_layout, char norm, char uplo, char diag,
                           lapack_int n, lapack_int kd, const float* ab,
                           lapack_int ldab, float* rcond );
lapack_int LAPACKE_dtbcon( int matrix_layout, char norm, char uplo, char diag,
                           lapack_int n, lapack_int kd, const double* ab,
                           lapack_int ldab, double* rcond );
lapack_int LAPACKE_ctbcon( int matrix_layout, char norm, char uplo, char diag,
                           lapack_int n, lapack_int kd,
                           const lapack_complex_float* ab, lapack_int ldab,
                           float* rcond );
lapack_int LAPACKE_ztbcon( int matrix_layout, char norm, char uplo, char diag,
                           lapack_int n, lapack_int kd,
                           const lapack_complex_double* ab, lapack_int ldab,
                           double* rcond );

lapack_int LAPACKE_stbrfs( int matrix_layout, char uplo, char trans, char diag,
                           lapack_int n, lapack_int kd, lapack_int nrhs,
                           const float* ab, lapack_int ldab, const float* b,
                           lapack_int ldb, const float* x, lapack_int ldx,
                           float* ferr, float* berr );
lapack_int LAPACKE_dtbrfs( int matrix_layout, char uplo, char trans, char diag,
                           lapack_int n, lapack_int kd, lapack_int nrhs,
                           const double* ab, lapack_int ldab, const double* b,
                           lapack_int ldb, const double* x, lapack_int ldx,
                           double* ferr, double* berr );
lapack_int LAPACKE_ctbrfs( int matrix_layout, char uplo, char trans, char diag,
                           lapack_int n, lapack_int kd, lapack_int nrhs,
                           const lapack_complex_float* ab, lapack_int ldab,
                           const lapack_complex_float* b, lapack_int ldb,
                           const lapack_complex_float* x, lapack_int ldx,
                           float* ferr, float* berr );
lapack_int LAPACKE_ztbrfs( int matrix_layout, char uplo, char trans, char diag,
                           lapack_int n, lapack_int kd, lapack_int nrhs,
                           const lapack_complex_double* ab, lapack_int ldab,
                           const lapack_complex_double* b, lapack_int ldb,
                           const lapack_complex_double* x, lapack_int ldx,
                           double* ferr, double* berr );

lapack_int LAPACKE_stbtrs( int matrix_layout, char uplo, char trans, char diag,
                           lapack_int n, lapack_int kd, lapack_int nrhs,
                           const float* ab, lapack_int ldab, float* b,
                           lapack_int ldb );
lapack_int LAPACKE_dtbtrs( int matrix_layout, char uplo, char trans, char diag,
                           lapack_int n, lapack_int kd, lapack_int nrhs,
                           const double* ab, lapack_int ldab, double* b,
                           lapack_int ldb );
lapack_int LAPACKE_ctbtrs( int matrix_layout, char uplo, char trans, char diag,
                           lapack_int n, lapack_int kd, lapack_int nrhs,
                           const lapack_complex_float* ab, lapack_int ldab,
                           lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_ztbtrs( int matrix_layout, char uplo, char trans, char diag,
                           lapack_int n, lapack_int kd, lapack_int nrhs,
                           const lapack_complex_double* ab, lapack_int ldab,
                           lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_stfsm( int matrix_layout, char transr, char side, char uplo,
                          char trans, char diag, lapack_int m, lapack_int n,
                          float alpha, const float* a, float* b,
                          lapack_int ldb );
lapack_int LAPACKE_dtfsm( int matrix_layout, char transr, char side, char uplo,
                          char trans, char diag, lapack_int m, lapack_int n,
                          double alpha, const double* a, double* b,
                          lapack_int ldb );
lapack_int LAPACKE_ctfsm( int matrix_layout, char transr, char side, char uplo,
                          char trans, char diag, lapack_int m, lapack_int n,
                          lapack_complex_float alpha,
                          const lapack_complex_float* a,
                          lapack_complex_float* b, lapack_int ldb );
lapack_int LAPACKE_ztfsm( int matrix_layout, char transr, char side, char uplo,
                          char trans, char diag, lapack_int m, lapack_int n,
                          lapack_complex_double alpha,
                          const lapack_complex_double* a,
                          lapack_complex_double* b, lapack_int ldb );

lapack_int LAPACKE_stftri( int matrix_layout, char transr, char uplo, char diag,
                           lapack_int n, float* a );
lapack_int LAPACKE_dtftri( int matrix_layout, char transr, char uplo, char diag,
                           lapack_int n, double* a );
lapack_int LAPACKE_ctftri( int matrix_layout, char transr, char uplo, char diag,
                           lapack_int n, lapack_complex_float* a );
lapack_int LAPACKE_ztftri( int matrix_layout, char transr, char uplo, char diag,
                           lapack_int n, lapack_complex_double* a );

lapack_int LAPACKE_stfttp( int matrix_layout, char transr, char uplo,
                           lapack_int n, const float* arf, float* ap );
lapack_int LAPACKE_dtfttp( int matrix_layout, char transr, char uplo,
                           lapack_int n, const double* arf, double* ap );
lapack_int LAPACKE_ctfttp( int matrix_layout, char transr, char uplo,
                           lapack_int n, const lapack_complex_float* arf,
                           lapack_complex_float* ap );
lapack_int LAPACKE_ztfttp( int matrix_layout, char transr, char uplo,
                           lapack_int n, const lapack_complex_double* arf,
                           lapack_complex_double* ap );

lapack_int LAPACKE_stfttr( int matrix_layout, char transr, char uplo,
                           lapack_int n, const float* arf, float* a,
                           lapack_int lda );
lapack_int LAPACKE_dtfttr( int matrix_layout, char transr, char uplo,
                           lapack_int n, const double* arf, double* a,
                           lapack_int lda );
lapack_int LAPACKE_ctfttr( int matrix_layout, char transr, char uplo,
                           lapack_int n, const lapack_complex_float* arf,
                           lapack_complex_float* a, lapack_int lda );
lapack_int LAPACKE_ztfttr( int matrix_layout, char transr, char uplo,
                           lapack_int n, const lapack_complex_double* arf,
                           lapack_complex_double* a, lapack_int lda );

lapack_int LAPACKE_stgevc( int matrix_layout, char side, char howmny,
                           const lapack_logical* select, lapack_int n,
                           const float* s, lapack_int lds, const float* p,
                           lapack_int ldp, float* vl, lapack_int ldvl,
                           float* vr, lapack_int ldvr, lapack_int mm,
                           lapack_int* m );
lapack_int LAPACKE_dtgevc( int matrix_layout, char side, char howmny,
                           const lapack_logical* select, lapack_int n,
                           const double* s, lapack_int lds, const double* p,
                           lapack_int ldp, double* vl, lapack_int ldvl,
                           double* vr, lapack_int ldvr, lapack_int mm,
                           lapack_int* m );
lapack_int LAPACKE_ctgevc( int matrix_layout, char side, 
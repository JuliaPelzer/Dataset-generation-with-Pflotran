/* HYPRE_config.h.  Generated from HYPRE_config.h.in by configure.  */
/******************************************************************************
 * Copyright 1998-2019 Lawrence Livermore National Security, LLC and other
 * HYPRE Project Developers. See the top-level COPYRIGHT file for details.
 *
 * SPDX-License-Identifier: (Apache-2.0 OR MIT)
 ******************************************************************************/

/* config/HYPRE_config.h.in.  Generated from configure.in by autoheader.  */

/* Release name */
#define HYPRE_RELEASE_NAME "hypre"

/* Version number */
#define HYPRE_RELEASE_VERSION "2.18.2"

/* Date of release */
#define HYPRE_RELEASE_DATE "2019/10/28"

/* Time of release */
#define HYPRE_RELEASE_TIME "00:00:00"

/* Bug reports */
#define HYPRE_RELEASE_BUGS "hypre-support@llnl.gov"

/* Define to 1 for Solaris. */
/* #undef HYPRE_SOLARIS */

/* Define to 1 for Linux on platforms running any version of CHAOS */
/* #undef HYPRE_LINUX_CHAOS */

/* Define to 1 for Linux platforms */
#define HYPRE_LINUX 1

/* Define to 1 for Alpha platforms */
/* #undef HYPRE_ALPHA */

/* Define to 1 for RS6000 platforms */
/* #undef HYPRE_RS6000 */

/* Define to 1 for IRIX64 platforms */
/* #undef HYPRE_IRIX64 */

/* Define to 1 if using long long int for HYPRE_BigInt */
/* #undef HYPRE_MIXEDINT */

/* Define to 1 if using long long int for HYPRE_Int and HYPRE_BigInt */
/* #undef HYPRE_BIGINT */

/* Define to 1 if using single precision values for HYPRE_Real */
/* #undef HYPRE_SINGLE */

/* Define to 1 if using quad precision values for HYPRE_Real */
/* #undef HYPRE_LONG_DOUBLE */

/* Define to 1 if using complex values */
/* #undef HYPRE_COMPLEX */

/* Define to be the max dimension size (must be at least 3) */
#define HYPRE_MAXDIM 3

/* Define to 1 if using persistent communication */
/* #undef HYPRE_USING_PERSISTENT_COMM */

/* Define to 1 if hopscotch hashing */
/* #undef HYPRE_HOPSCOTCH */

/* Define to 1 if an MPI library is found */
#define HYPRE_HAVE_MPI 1

/* Define to 1 if Node Aware MPI library is used */
/* #undef HYPRE_USING_NODE_AWARE_MPI */

/* Define to 1 if the routine MPI_Comm_f2c is found */
#define HYPRE_HAVE_MPI_COMM_F2C 1

/* Disable MPI, enable serial codes */
/* #undef HYPRE_SEQUENTIAL */

/* Using HYPRE timing routines */
/* #undef HYPRE_TIMING */

/* Using dxml for BLAS */
/* #undef HYPRE_USING_DXML */

/* Using essl for BLAS */
/* #undef HYPRE_USING_ESSL */

/* Using internal Hypre routines */
/* #undef HYPRE_USING_HYPRE_BLAS */

/* Using internal Hypre routines */
/* #undef HYPRE_USING_HYPRE_LAPACK */

/* No global partitioning being used */
#define HYPRE_NO_GLOBAL_PARTITION 1

/* Print HYPRE errors */
/* #undef HYPRE_PRINT_ERRORS */

/* Enable OpenMP support */
/* #undef HYPRE_USING_OPENMP */

/*- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 * MEMORY
 *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -*/

/* Define to 1 if using host memory only */
#define HYPRE_USING_HOST_MEMORY 1

/* Define to 1 if using device memory without UM */
/* #undef HYPRE_USING_DEVICE_MEMORY */

/* Define to 1 if using unified memory */
/* #undef HYPRE_USING_UNIFIED_MEMORY */

/*- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 * EXECUTION
 *- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -*/
/* Define to 1 if executing on device with CUDA */
/* #undef HYPRE_USING_CUDA */

/* Define to 1 if executing on device with OpenMP  */
/* #undef HYPRE_USING_DEVICE_OPENMP */

/* Define to 1 if using OpenMP on device [target alloc version] */
/* #undef HYPRE_DEVICE_OPENMP_ALLOC */

/* Define to 1 if using OpenMP on device [target mapped version] */
/* #undef HYPRE_DEVICE_OPENMP_MAPPED */

/* Define to 1 if strictly checking OpenMP offload directives */
/* #undef HYPRE_DEVICE_OPENMP_CHECK */

/* Define to 1 if executing on host/device with RAJA */
/* #undef HYPRE_USING_RAJA */

/* Define to 1 if executing on host/device with KOKKOS */
/* #undef HYPRE_USING_KOKKOS */

/* Define to 1 if using NVIDIA Tools Extension (NVTX) */
/* #undef HYPRE_USING_NVTX */

/* Define to 1 if using cuSPARSE */
/* #undef HYPRE_USING_CUSPARSE */

/* Define to 1 if using cuBLAS */
/* #undef HYPRE_USING_CUBLAS */

/* Define to 1 if using cuRAND */
/* #undef HYPRE_USING_CURAND */

/* Define to 1 if using GPU aware MPI */
/* #undef HYPRE_WITH_GPU_AWARE_MPI */

/* Define to 1 if using CUDA streams */
#define HYPRE_USING_CUDA_STREAMS 1

/* Define as follows to set the Fortran name mangling scheme:
 * 0 = unspecified
 * 1 = no underscores
 * 2 = one underscore
 * 3 = two underscores
 * 4 = caps, no underscores
 * 5 = one underscore before and after */
#define HYPRE_FMANGLE 0

/* Define as in HYPRE_FMANGLE to set the BLAS name mangling scheme */
#define HYPRE_FMANGLE_BLAS 0

/* Define as in HYPRE_FMANGLE to set the LAPACK name mangling scheme */
#define HYPRE_FMANGLE_LAPACK 0

/* Define to a macro mangling the given C identifier (in lower and upper
 * case), which must not contain underscores, for linking with Fortran. */
#define HYPRE_FC_FUNC(name,NAME) name ## _

/* As HYPRE_HYPRE_FC_FUNC, but for C identifiers containing underscores. */
#define HYPRE_FC_FUNC_(name,NAME) name ## _

/* Define to 1 if Caliper instrumentation is enabled */
/* #undef HYPRE_USING_CALIPER */

/* Define to 1 if using SuperLU */
/* #undef HAVE_SUPERLU */

/* Define to 1 if using DSuperLU */
/* #undef HYPRE_USING_DSUPERLU */

/* Define to 1 if using MLI */
/* #undef HAVE_MLI */

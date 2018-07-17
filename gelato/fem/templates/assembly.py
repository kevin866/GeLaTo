# coding: utf-8

# .............................................
#          ASSEMBLY OF BILINEAR FORM 1D case - scalar
# .............................................
_assembly_bilinear_1d_scalar = """
def {__ASSEMBLY_NAME__}( self, test_space, trial_space{__ARGS__} ):
    {__DOCSTRING__}
    # Sizes
    [s1] = test_space.vector_space.starts
    [e1] = test_space.vector_space.ends

    [test_p1] = test_space.vector_space.pads
    [trial_p1] = trial_space.vector_space.pads

    # Quadrature data
    k1        = test_space.quad_order
    points_1  = test_space.quad_points
    weights_1 = test_space.quad_weights

    test_spans_1   = test_space.spans

    test_basis_1   = test_space.quad_basis
    trial_basis_1  = trial_space.quad_basis

    # Create global matrices
    from spl.linalg.stencil import StencilMatrix
    M = StencilMatrix( test_space.vector_space, trial_space.vector_space )

    # Create element matrices
    from numpy import zeros
    mat = zeros( (test_p1+1,2*trial_p1+1) )

    # Build global matrices: cycle over elements
    for ie1 in range(s1, e1+1-test_p1):

        # Get spline index, B-splines' values and quadrature weights
        is1 =   test_spans_1[ie1]

        w1  = weights_1[ie1,:]
        u1  = points_1[ie1, :]

        test_bs1  = test_basis_1[ie1,:,:,:]

        trial_bs1 = trial_basis_1[ie1,:,:,:]

        # Compute element matrices
        {__KERNEL_NAME__}( test_p1, trial_p1, k1, test_bs1, trial_bs1, u1, w1, mat{__ARGS__} )

        # Update global matrices
        M[is1-test_p1:is1+1,:] += mat[:,:]

    return M
"""
# .............................................

# .............................................
#          ASSEMBLY OF LINEAR FORM 1D case - scalar
# .............................................
_assembly_linear_1d_scalar = """
def {__ASSEMBLY_NAME__}( self, test_space{__ARGS__} ):
    {__DOCSTRING__}
    # Sizes
    [s1] = test_space.vector_space.starts
    [e1] = test_space.vector_space.ends

    [test_p1] = test_space.vector_space.pads

    # Quadrature data
    k1        = test_space.quad_order
    points_1  = test_space.quad_points
    weights_1 = test_space.quad_weights

    test_spans_1   = test_space.spans

    test_basis_1   = test_space.quad_basis

    # Create global matrices
    from spl.linalg.stencil import StencilVector
    rhs = StencilVector( test_space.vector_space )

    # Create element matrices
    from numpy import zeros
    mat = zeros( test_p1+1 )

    # Build global matrices: cycle over elements
    for ie1 in range(s1, e1+1-test_p1):

        # Get spline index, B-splines' values and quadrature weights
        is1 =   test_spans_1[ie1]

        w1  = weights_1[ie1,:]
        u1  = points_1[ie1, :]

        test_bs1  = test_basis_1[ie1,:,:,:]

        # Compute element matrices
        {__KERNEL_NAME__}( test_p1, k1, test_bs1, u1, w1, mat{__ARGS__} )

        # Update global vectors
        rhs[is1-test_p1:is1+1] += mat[:]

    return rhs
"""
# .............................................

# .............................................
#          ASSEMBLY OF BILINEAR FORM 2D case - scalar
# .............................................
_assembly_bilinear_2d_scalar = """
def {__ASSEMBLY_NAME__}( self, test_space, trial_space{__ARGS__} ):
    {__DOCSTRING__}
    # Sizes
    [s1, s2] = test_space.vector_space.starts
    [e1, e2] = test_space.vector_space.ends

    [test_p1, test_p2] = test_space.vector_space.pads
    [trial_p1, trial_p2] = trial_space.vector_space.pads

    # Quadrature data
    [k1, k2] = [W.quad_order for W in test_space.spaces]
    [points_1, points_2] = [W.quad_points for W in test_space.spaces]
    [weights_1, weights_2] = [W.quad_weights for W in test_space.spaces]

    [test_spans_1, test_spans_2] = [W.spans for W in test_space.spaces]

    [test_basis_1, test_basis_2] = [W.quad_basis for W in test_space.spaces]
    [trial_basis_1, trial_basis_2] = [W.quad_basis for W in trial_space.spaces]

    # Create global matrices
    from spl.linalg.stencil import StencilMatrix
    M = StencilMatrix( test_space.vector_space, trial_space.vector_space )

    # Create element matrices
    from numpy import zeros
    mat = zeros( (test_p1+1, test_p2+1, 2*trial_p1+1, 2*trial_p2+1) )

    # Build global matrices: cycle over elements
    for ie1 in range(s1, e1+1-test_p1):
        for ie2 in range(s2, e2+1-test_p2):

            # Get spline index, B-splines' values and quadrature weights
            is1 = test_spans_1[ie1]
            is2 =   test_spans_2[ie2]

            w1  = weights_1[ie1,:]
            w2  = weights_2[ie2,:]

            u1  = points_1[ie1,:]
            u2  = points_2[ie2,:]

            test_bs1  = test_basis_1[ie1,:,:,:]
            test_bs2  = test_basis_2[ie2,:,:,:]

            trial_bs1 = trial_basis_1[ie1,:,:,:]
            trial_bs2 = trial_basis_2[ie2,:,:,:]

            # Compute element matrices
            {__KERNEL_NAME__}( test_p1, test_p2, trial_p1, trial_p2, k1, k2, test_bs1, test_bs2, trial_bs1, trial_bs2, u1, u2, w1, w2, mat{__ARGS__} )

            # Update global matrices
            M[is1-test_p1:is1+1, is2-test_p2:is2+1, :, :] += mat[:,:,:,:]

    return M
"""
# .............................................

# .............................................
#          ASSEMBLY OF LINEAR FORM 2D case - scalar
# .............................................
_assembly_linear_2d_scalar = """
def {__ASSEMBLY_NAME__}( self, test_space{__ARGS__} ):
    {__DOCSTRING__}
    # Sizes
    [s1, s2] = test_space.vector_space.starts
    [e1, e2] = test_space.vector_space.ends

    [test_p1, test_p2] = test_space.vector_space.pads

    # Quadrature data
    [k1, k2] = [W.quad_order for W in test_space.spaces]
    [points_1, points_2] = [W.quad_points  for W in test_space.spaces]
    [weights_1, weights_2] = [W.quad_weights for W in test_space.spaces]

    [test_spans_1, test_spans_2] = [W.spans for W in test_space.spaces]

    [test_basis_1, test_basis_2] = [W.quad_basis for W in test_space.spaces]

    # Create global matrices
    from spl.linalg.stencil import StencilVector
    rhs = StencilVector( test_space.vector_space )

    # Create element matrices
    from numpy import zeros
    mat = zeros( (test_p1+1, test_p2+1) )

    # Build global matrices: cycle over elements
    for ie1 in range(s1, e1+1-test_p1):
        for ie2 in range(s2, e2+1-test_p2):

            # Get spline index, B-splines' values and quadrature weights
            is1 = test_spans_1[ie1]
            is2 =   test_spans_2[ie2]

            w1  = weights_1[ie1,:]
            w2  = weights_2[ie2,:]

            u1  = points_1[ie1,:]
            u2  = points_2[ie2,:]

            test_bs1  = test_basis_1[ie1,:,:,:]
            test_bs2  = test_basis_2[ie2,:,:,:]

            # Compute element matrices
            {__KERNEL_NAME__}( test_p1, test_p2, k1, k2, test_bs1, test_bs2, u1, u2, w1, w2, mat{__ARGS__} )

            # Update global matrices
            rhs[is1-test_p1:is1+1, is2-test_p2:is2+1] += mat[:,:]

    return rhs
"""
# .............................................

# .............................................
#          ASSEMBLY OF BILINEAR FORM 3D case - scalar
# .............................................
_assembly_bilinear_3d_scalar = """
def {__ASSEMBLY_NAME__}( self, test_space, trial_space{__ARGS__} ):
    {__DOCSTRING__}
    # Sizes
    [s1, s2, s3] = test_space.vector_space.starts
    [e1, e2, e3] = test_space.vector_space.ends

    [test_p1, test_p2, test_p3] = test_space.vector_space.pads
    [trial_p1, trial_p2, trial_p3] = trial_space.vector_space.pads

    # Quadrature data
    [k1, k2, k3] = [W.quad_order for W in test_space.spaces]
    [points_1, points_2, points_3] = [W.quad_points  for W in test_space.spaces]
    [weights_1, weights_2, weights_3] = [W.quad_weights for W in test_space.spaces]

    [test_spans_1, test_spans_2, test_spans_3] = [W.spans for W in test_space.spaces]

    [test_basis_1, test_basis_2, test_basis_3] = [W.quad_basis for W in test_space.spaces]
    [trial_basis_1, trial_basis_2, trial_basis_3] = [W.quad_basis for W in trial_space.spaces]

    # Create global matrices
    from spl.linalg.stencil import StencilMatrix
    M = StencilMatrix( test_space.vector_space, trial_space.vector_space )

    # Create element matrices
    from numpy import zeros
    mat = zeros( (test_p1+1, test_p2+1, test_p3+1, 2*trial_p1+1, 2*trial_p2+1, 2*trial_p3+1) )

    # Build global matrices: cycle over elements
    for ie1 in range(s1, e1+1-test_p1):
        for ie2 in range(s2, e2+1-test_p2):
            for ie3 in range(s3, e3+1-test_p3):

                # Get spline index, B-splines' values and quadrature weights
                is1 = test_spans_1[ie1]
                is2 = test_spans_2[ie2]
                is3 = test_spans_3[ie3]

                w1  = weights_1[ie1,:]
                w2  = weights_2[ie2,:]
                w3  = weights_3[ie3,:]

                u1  = points_1[ie1,:]
                u2  = points_2[ie2,:]
                u3  = points_3[ie3,:]

                test_bs1  = test_basis_1[ie1,:,:,:]
                test_bs2  = test_basis_2[ie2,:,:,:]
                test_bs3  = test_basis_3[ie3,:,:,:]

                trial_bs1 = trial_basis_1[ie1,:,:,:]
                trial_bs2 = trial_basis_2[ie2,:,:,:]
                trial_bs3 = trial_basis_3[ie3,:,:,:]

                # Compute element matrices
                {__KERNEL_NAME__}( test_p1, test_p2, test_p3, trial_p1, trial_p2, trial_p3, k1, k2, k3, test_bs1, test_bs2, test_bs3, trial_bs1, trial_bs2, trial_bs3, u1, u2, u3, w1, w2, w3, mat{__ARGS__} )

                # Update global matrices
                M[is1-test_p1:is1+1, is2-test_p2:is2+1, is3-test_p3:is3+1, :, :, :] += mat[:,:,:,:,:,:]

    return M
"""
# .............................................

# .............................................
#          ASSEMBLY OF LINEAR FORM 3D case - scalar
# .............................................
_assembly_linear_3d_scalar = """
def {__ASSEMBLY_NAME__}( self, test_space{__ARGS__} ):
    {__DOCSTRING__}
    # Sizes
    [s1, s2, s3] = test_space.vector_space.starts
    [e1, e2, e3] = test_space.vector_space.ends

    [test_p1, test_p2, test_p3] = test_space.vector_space.pads

    # Quadrature data
    [k1, k2, k3] = [W.quad_order for W in test_space.spaces]
    [points_1, points_2, points_3] = [W.quad_points  for W in test_space.spaces]
    [weights_1, weights_2, weights_3] = [W.quad_weights for W in test_space.spaces]

    [test_spans_1, test_spans_2, test_spans_3] = [W.spans for W in test_space.spaces]

    [test_basis_1, test_basis_2, test_basis_3] = [W.quad_basis for W in test_space.spaces]

    # Create global matrices
    from spl.linalg.stencil import StencilVector
    rhs = StencilVector( test_space.vector_space )

    # Create element matrices
    from numpy import zeros
    mat = zeros( (test_p1+1, test_p2+1, test_p3+1) )

    # Build global matrices: cycle over elements
    for ie1 in range(s1, e1+1-test_p1):
        for ie2 in range(s2, e2+1-test_p2):
            for ie3 in range(s3, e3+1-test_p3):

                # Get spline index, B-splines' values and quadrature weights
                is1 = test_spans_1[ie1]
                is2 = test_spans_2[ie2]
                is3 = test_spans_3[ie3]

                w1  = weights_1[ie1,:]
                w2  = weights_2[ie2,:]
                w3  = weights_3[ie3,:]

                u1  = points_1[ie1,:]
                u2  = points_2[ie2,:]
                u3  = points_3[ie3,:]

                test_bs1  = test_basis_1[ie1,:,:,:]
                test_bs2  = test_basis_2[ie2,:,:,:]
                test_bs3  = test_basis_3[ie3,:,:,:]

                # Compute element matrices
                {__KERNEL_NAME__}( test_p1, test_p2, test_p3, k1, k2, k3, test_bs1, test_bs2, test_bs3, u1, u2, u3, w1, w2, w3, mat{__ARGS__} )

                # Update global matrices
                rhs[is1-test_p1:is1+1, is2-test_p2:is2+1, is3-test_p3:is3+1] += mat[:,:,:]

    return rhs
"""
# .............................................
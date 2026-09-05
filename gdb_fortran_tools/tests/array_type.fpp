! declare 
#:set TYPES = [('i4' , 'integer(kind=4)' , 'int'  ),&
               ('i8' , 'integer(kind=8)' , 'int'  ),& 
               ('r4' , 'real(kind=4)'    , 'real' ),&
               ('r8' , 'real(kind=8)'    , 'real' ),&
               ('c8' , 'complex(kind=4)' , 'cmplx'),&
               ('c16', 'complex(kind=8)' , 'cmplx')]

#:def dupdim(i)
#{for j in range(i-1)}#:,#{endfor}#:
#:enddef

#:set MAX_DIM = 3

program test_array
 implicit none
 integer, parameter :: MAX_DIM = ${MAX_DIM}$
 integer :: i
 integer, parameter :: N  = product([(i,i=1,MAX_DIM)])

#:for id in range(1,MAX_DIM+1)
  #:for type_name, type_decl, cv in TYPES
     call test_${type_name}$_${id}$d()
  #:endfor
  call test_logical_${id}$d()
#:endfor

contains
#:for id in range(1,MAX_DIM+1)
   #:for type_name, type_decl, cv in TYPES
     subroutine test_${type_name}$_${id}$d()
        integer :: i
        ${type_decl}$, allocatable :: a(${dupdim(id)}$)
        a = reshape([(${cv}$(i),i=1,N)],[product([(i,i=max_dim,${id}$,-1)]),(i,i=(${id}$-1),1,-1)])
        print *, sum(a)
     end subroutine test_${type_name}$_${id}$d
  #:endfor
  subroutine test_logical_${id}$d()
     integer :: i
     logical, allocatable :: a(${dupdim(id)}$)
     a = reshape([(.true.,i=1,N)],[product([(i,i=max_dim,${id}$,-1)]),(i,i=(${id}$-1),1,-1)])
     print *, any(a)
  end subroutine test_logical_${id}$d
#:endfor
end program test_array

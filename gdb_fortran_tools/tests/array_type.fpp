#:set TYPES = [('i4' , 'integer(kind=4)' , 'int'  ),&
               ('i8' , 'integer(kind=8)' , 'int'  ),& 
               ('r4' , 'real(kind=4)'    , 'real' ),&
               ('r8' , 'real(kind=8)'    , 'real' ),&
               ('c4' , 'complex(kind=4)' , 'cmplx'),&
               ('c8', 'complex(kind=8)' , 'cmplx')]
#:def dupdim(i)
#{for j in range(i-1)}#:,#{endfor}#:
#:enddef
#:set MAX_DIM = 6
program test_array
 use iso_fortran_env
 implicit none
 integer, parameter :: MAX_DIM = ${MAX_DIM}$
 integer :: i
 integer, parameter :: N  = product([(i,i=1,MAX_DIM)])
 
 character(len=256) :: name_test

 call get_command_argument(1, name_test)

 select case(trim(name_test))

#:for id in range(1,MAX_DIM+1)
  #:for type_name, type_decl, cv in TYPES
    case("${type_name}$_${id}$d") 
        call test_${type_name}$_${id}$d()
  #:endfor
    case("logical_${id}$d") 
        call test_logical_${id}$d()
#:endfor
  case default
  end select
contains
#:for id in range(1,MAX_DIM+1)
   #:for type_name, type_decl, cv in TYPES
     subroutine test_${type_name}$_${id}$d()
        integer :: i
        ${type_decl}$, allocatable :: a(${dupdim(id)}$)
        a = reshape([(${cv}$(i),i=1,N)],[product([(i,i=max_dim,${id}$,-1)]),(i,i=(${id}$-1),1,-1)])
        print '(a,i0)', "sum = ", nint(real(sum(a)))
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

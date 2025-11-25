#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Patch asyncio to allow nested event loops
Summary(pl.UTF-8):	Łatka na asyncio pozwalająca na zagnieżdżone pętle zdarzeń
Name:		python3-nest-asyncio
Version:	1.6.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/nest-asyncio/
Source0:	https://files.pythonhosted.org/packages/source/n/nest-asyncio/nest_asyncio-%{version}.tar.gz
# Source0-md5:	4a15c56d692367a24ea12072e2e475f3
URL:		https://pypi.org/project/nest-asyncio/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 1:42
BuildRequires:	python3-setuptools_scm >= 3.4.3
BuildRequires:	python3-wheel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module patches asyncio to allow nested use of asyncio.run and
loop.run_until_complete.

%description -l pl.UTF-8
Ten moduł modyfikuje bibliotekę asyncio, aby pozwalała na zagnieżdżone
używanie asyncio.run i loop.run_until_complete.

%prep
%setup -q -n nest_asyncio-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} tests/nest_test.py
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/nest_asyncio.py
%{py3_sitescriptdir}/__pycache__/nest_asyncio.cpython-*.py[co]
%{py3_sitescriptdir}/nest_asyncio-%{version}.dist-info

# Conditional build:
%bcond_with	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	nest_asyncio
Summary:	Patch asyncio to allow nested event loops
Name:		python3-nest-asyncio
Version:	1.6.0
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/n/nest-asyncio/nest_asyncio-%{version}.tar.gz
# Source0-md5:	4a15c56d692367a24ea12072e2e475f3
URL:		https://pypi.org/project/nest-asyncio/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
#BuildRequires:	python3-
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module patches asyncio to allow nested use of asyncio.run and
loop.run_until_complete.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n nest_asyncio-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-doc
PYTHONPATH=$(pwd)/build-3-doc \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/*%{module}*
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif

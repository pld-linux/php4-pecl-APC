%define		_modname	APC
%define		_status		stable
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	%{_modname} - Alternative PHP Cache
Summary(pl):	%{_modname} - alternatywne cache PHP
Name:		php4-pecl-%{_modname}
Version:	3.0.11
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	4d4481ba7be4245320083b9b254d6d79
URL:		http://pecl.php.net/package/APC/
BuildRequires:	php4-devel >= 3:4.3.0
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
APC is the Alternative PHP Cache. It was conceived of to provide a
free, open, and robust framework for caching and optimizing PHP
intermediate code.

In PECL status of this package is: %{_status}.

%description -l pl
APC to alternatywne cache PHP. W wyobra�eniach mia�o dostarcza�
wolnodost�pny, otwarty i pot�ny szkielet do buforowania i
optymalizowania kodu po�redniego PHP.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
export CPPFLAGS="-DAPC_PHP4_STAT"
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/apc.so $RPM_BUILD_ROOT%{extensionsdir}/%{_modname}.so
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
apc.enabled=1
;apc.optimization=0
;apc.shm_segments=1
;apc.shm_size=32
;apc.cache_by_default=1
;apc.max_file_size=1M
;apc.num_files_hint=1024
;apc.gc_ttl=3600
;apc.ttl=0
;apc.mmap_file_mask=/tmp/apc.XXXXXX
;apc.filters=
;apc.stat=1
;apc.enable_cli=0
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CHANGELOG,INSTALL,NOTICE}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so

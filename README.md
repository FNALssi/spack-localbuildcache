

## Spack-localbuildcache

a [Spack extension](https://spack.readthedocs.io/en/latest/extensions.html#custom-extensions) to make a buildcache of the current environment, excluding packages in upstream spack instances.
It also writes a "reconstitute.sh" script that can be run in grid jobs to recareate this envrionment in a grid job, etc. that can see a copy of this buildcache.
The buildcache is put in the current environent directory's "bc" subdirectory.

### Usage

In most cases you can just do:

  spack localbuildcache

but there are a few option flags that are often useful
  
* --key name specifies the signing key name; this assumes the signing key has been configured in the spack gnupg area.

### Installation

After cloning the repository somewhere, See the [Spack docs](https://spack.readthedocs.io/en/latest/extensions.html#configure-spack-to-use-extensions) on adding the path to config.yaml under 'extensions:'

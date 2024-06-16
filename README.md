# reckless-wrapper

A CLN plugin that exposes the reckless shell script functionality as CLN RPC methods.

## Source Management


### Add Trusted GPG Keys

> TODO there needs to be a way to upload/identify GPG pubkey that is trusted. Then when adding source, logic will ensure that GPG signatures are checked on git tags.


### List Source Repos

`lightning-cli.sh reckless-source list`
```json
{
   "sources": [
      "https://github.com/lightningd/plugins"
   ]
}
```

### Add a source repo with CLN plugin code

If you're developing a new plugin, you can add it as a source:

`lightning-cli.sh reckless-source add https://github.com/userx/some-other-cln-plugin`

```json
{
   "sources": [
      "https://github.com/lightningd/plugins",
      "https://github.com/userx/some-other-cln-plugin"
   ]
}
```

### Remove a source repo

You can remove the source:

`lightning-cli.sh reckless-source remove https://github.com/userx/some-other-cln-plugin`

```json
{
   "sources": [
      "https://github.com/lightningd/plugins"
   ]
}
```

## Installing a plugin

> TODO adovcate that we move this under `lightning-cli plugin install`

Just having the source defined is not enough! You have to run the `reckless install` command before the plugin becomes available.

`lightning-cli.sh reckless install bolt12-prism`

```json
TODO
```

### Uninstalling a plugin

`lightning-cli.sh reckless uninstall bolt12-prism`
```json
{
   "uninstall_output": [
      "bolt12-prism disabled",
      "bolt12-prism uninstalled successfully."
   ]
}
```
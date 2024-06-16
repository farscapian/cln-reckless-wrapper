# reckless-wrapper

A CLN plugin that exposes the reckless shell script functionality as CLN RPC methods.

## Source Management

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

Similarly, if you're developing a new plugin, you can add it as a source:

`lightning-cli.sh reckless-source remove https://github.com/userx/some-other-cln-plugin`

```json
{
   "sources": [
      "https://github.com/lightningd/plugins"
   ]
}
```

## Installing a plugin

Just having the source defined is not enough! You have to run the `reckless install` command.

`lightning-cli.sh reckless install bolt12-prism`

```json

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
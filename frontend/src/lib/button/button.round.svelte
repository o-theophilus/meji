<script>
	import { Button } from '.';
	let { ...props } = $props();
</script>

<Button
	{...props}
	--button-padding-x="var(--button-padding-x_, 0)"
	--button-width="var(--button-width_, 32px)"
	--button-height="var(--button-height_, 32px)"
	--button-border-radius="var(--button-border-radius_, 50%)"
></Button>

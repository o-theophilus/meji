<script>
	import { Button } from '.';
	let { ...props } = $props();
</script>

<div>
	<Button
		{...props}
		--button-padding-x="var(--button-padding-x_, 0)"
		--button-width="var(--button-width_, 32px)"
		--button-height="var(--button-height_, 32px)"
		--button-border-radius="var(--button-border-radius_, 50%)"
		--button-background-color="var(--button-background-color_, transparent)"
		--button-color-hover="var(--button-color-hover_, var(--ft1))"
		--button-background-color-hover="var(--button-background-color-hover_, transparent)"
		--button-outline-color="var(--button-outline-color_, transparent)"
		--button-outline-color-hover="var(--button-outline-color-hover_, var(--ft2))"
	></Button>
</div>

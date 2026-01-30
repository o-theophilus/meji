<script>
	let { value } = $props();

	let v = value.split(':');
	let label = v[0];
	let color = v[1];
</script>

{label}
{#if color}
	<span
		class="color"
		style="
		background-color: {color};
		outline: 1px solid light-dark(hsl(0, 0%, 85%), hsl(0, 0%, 25%));
		display: inline-block;
		height: 8px;
		width: 16px;
		border-radius: 4px;
		flex-shrink: 0;"
	></span>
{/if}

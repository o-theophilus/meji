<script>
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	let disabled = false;
</script>

<Button
	class="round"
	on:click={() => {
		window.history.back();
		disabled = true;
	}}
	{disabled}
>
	<SVG type="angle" size="10" />
</Button>

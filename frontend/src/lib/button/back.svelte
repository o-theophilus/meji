<script>
	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';

	let disabled = false;
</script>

<BRound
	size="large"
	on:click={() => {
		window.history.back();
		disabled = true;
	}}
	{disabled}
>
	<SVG type="angle" size="10" />
</BRound>

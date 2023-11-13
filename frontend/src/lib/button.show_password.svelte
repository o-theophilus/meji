<script>
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let show_password = false;
</script>

<form on:submit|preventDefault>
	<Button
		class="round"
		on:click={() => {
			show_password = !show_password;
		}}
	>
		<SVG type={show_password ? 'hide_password' : 'show_password'} size="12" />
	</Button>
</form>

<style>
	form {
		position: absolute;
		right: var(--sp1);
		top: 0;

		display: flex;
		align-items: center;

		height: 100%;
	}
</style>

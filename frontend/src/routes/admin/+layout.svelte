<script>
	import Nav from './admin_nav.svelte';

	let { children } = $props();

	let ops = $state({ open: true });
</script>

<div class="container">
	<Nav bind:ops></Nav>

	<div class="page">
		{@render children()}
	</div>
</div>

<style>
	.container {
		display: flex;
		/* align-items: flex-end; */
		background-color: var(--bg1);
	}

	.page {
		width: 100%;
	}
</style>

<script>
	import Card from '$lib/card.svelte';
	import Center from '$lib/center.svelte';
	import Button from '$lib/button.svelte';
	import Meta from '$lib/meta.svelte';
	import SVG from '$lib/svg.svelte';

	import { page } from '$app/stores';
</script>

<Meta title="Error" description="Error" />

<Center>
	<br />
	<div class="title">Error</div>
</Center>

<Card>
	<div class="title">{$page.status}</div>
	{@html $page.error.message}
	<br />
	<br />

	<Button
		on:click={() => {
			document.location = '/';
		}}
	>
		<SVG type="home" />
		Home
	</Button>
</Card>

<style>
	.title {
		color: var(--ac1);
		font-weight: 600;
	}
</style>

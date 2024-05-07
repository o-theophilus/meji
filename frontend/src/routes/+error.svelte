<script>
	import Card from '$lib/card.svelte';
	import Center from '$lib/center.svelte';
	import Button from '$lib/button/button.svelte';
	import Meta from '$lib/meta.svelte';
	import SVG from '$lib/svg.svelte';
	import Log from '$lib/log.svelte';
	import Title from '$lib/title.svelte';

	import { page } from '$app/stores';
</script>

<Meta title="Error" description={$page.error.message} />
<Log entity_type={'page'} status="400" />

<Center>
	<Title>Error</Title>
</Center>

<Card>
	<div class="bold">{$page.status}</div>
	{@html $page.error.message}
	<br />
	<br />

	<Button
		on:click={() => {
			document.location = '/';
		}}
	>
		<SVG icon="home" />
		Home
	</Button>
</Card>

<style>
	.bold {
		color: var(--ac1);
		font-weight: 900;
	}
</style>

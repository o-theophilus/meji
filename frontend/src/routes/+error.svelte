<script>
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Meta from '$lib/meta.svelte';
	import SVG from '$lib/svg.svelte';

	import { page } from '$app/stores';
</script>

<Meta title="Error" description="Error" />

<Card>
	<div class="title">{$page.status}</div>
	<div class="body">
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
	</div>
</Card>

<style>
	.title {
		font-weight: 600;
	}
	.body {
		margin-top: var(--sp4);
	}
</style>

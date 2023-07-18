<script>
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Meta from '$lib/meta.svelte';

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
			name="Home"
			icon="home"
			on:click={() => {
				document.location = '/';
			}}
		/>
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

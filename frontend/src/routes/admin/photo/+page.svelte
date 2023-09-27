<script>
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';

	export let data;
	let { missing } = data;
	let { unused } = data;
</script>

<Meta title="Activity" description="Activity" />

<Card>
	<b> Manage Photos</b>
	<br />
	<br />
	<span class="bold"> Missing Photos</span>
	<br />
	<br />
	{#each missing as x}
		<a href="/{x.slug}">{x.name}</a>

		<br />
	{:else}
		no item here
	{/each}
	<br />
	<br />
	<span class="bold"> Unused Photos </span>
	<br />
	<br />
	{#each unused as x}
		<img src={`${x}/100` || '/image/item.png'} alt="missing" onerror="this.src='/image/item.png'" />
	{:else}
		no item here
	{/each}
</Card>

<style>
	.bold {
		font-weight: 500;
	}
</style>

<script>
	import Button from '$lib/button.svelte';

	export let log;
	
	let href = '';

	if (log.entity.type == 'item') {
		href = ``;
	} else if (log.entity.type == 'order') {
		href = `/orders`;
	} else if (log.entity.type == 'voucher') {
		href = `/admin/vouchers`;
	}

	href = `${href}/${log.entity.key}`;
</script>

<section>
	{log.date}
	<span class="status" class:error={log.status == 400}>
		{log.status}
	</span>
	<br />
	<Button class="link" href="/profile?search={log.user.key}">
		{log.user.name}
	</Button>

	:
	{log.action}
	<Button class="link" {href}>
		{#if log.entity.name}
			{log.entity.name}
		{:else}
			{log.entity.key}
		{/if}
	</Button>

	{#if log.misc}
		{#each Object.entries(log.misc) as [key, value]}
			<br />
			{key}: {value}
		{/each}
	{/if}
</section>

<style>
	section {
		padding: var(--sp0) 0;
	}
	section:not(:last-child) {
		border-bottom: 2px solid var(--ac4);
	}

	.status {
		background-color: var(--cl5);
		color: var(--ac5_);
	}
	.error {
		background-color: var(--cl4);
	}
</style>

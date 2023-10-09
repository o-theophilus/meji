<script>
	import Button from '$lib/button.svelte';

	export let log;

	let href = '';
	if (log.entity.type == 'item') {
		href = `/${log.entity.key}`;
	} else if (log.entity.type == 'order') {
		href = `/orders/${log.entity.key}`;
	} else if (log.entity.type == 'voucher') {
		href = `/admin/vouchers/${log.entity.key}`;
	} else if (log.entity.type == 'advert') {
		href = `/${log.entity.key.split('_')[0]}?edit=true&advert=true`;
	}
</script>

<section>
	<div
		class="status"
		class:good={log.status == 200}
		class:caution={![200, 400].includes(log.status)}
		class:error={log.status == 400}
	/>
	{log.date}
	<br />

	<Button class="link" href="/profile?search={log.user.key}">
		{log.user.name}
	</Button>

	{log.action}
	{log.entity.type}

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
		padding: var(--sp2) 0;
		border-bottom: 1px solid var(--ac4);
	}

	.status {
		display: inline-block;
		--size: 10px;
		width: var(--size);
		height: var(--size);

		border-radius: 50%;

		background-color: var(--cl5);
		color: var(--ac5_);
	}
	.good {
		background-color: var(--cl5);
	}
	.caution {
		background-color: var(--cl3);
	}
	.error {
		background-color: var(--cl4);
	}
</style>

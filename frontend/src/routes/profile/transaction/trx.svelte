<script>
	import Link from '$lib/button/link.svelte';

	export let trx;

	let href = '';
	if (trx.entity_type == 'order') {
		href = `/orders/${trx.entity}`;
	} else if (trx.entity_type == 'voucher') {
		href = `/admin/vouchers/${trx.entity_key}`;
	}
</script>

<section>
	<div
		class="status"
		class:good={trx.status == 200}
		class:caution={![200, 400].includes(trx.status)}
		class:error={trx.status == 400}
	/>

	<span class="date">
		{trx.date.split('T').join(' ')}
	</span>

	<div
		class="status"
		class:good={trx.direction == 'credit'}
		class:error={trx.direction == 'debit'}
	/>
	<span class="date">
		{trx.direction}
	</span>
	<br />

	{trx.entity_type}

	<Link {href}>
		{trx.entity_key}
	</Link>

	{#if trx.misc}
		{#each Object.entries(trx.misc) as [key, value]}
			<br />
			{key}: {value}
		{/each}
	{/if}
</section>

<style>
	section:not(:first-of-type) {
		margin-top: var(--sp2);
		padding-top: var(--sp2);
		border-top: 2px solid var(--ac5);
	}

	.status {
		display: inline-block;
		--size: 10px;
		width: var(--size);
		height: var(--size);

		border-radius: 50%;

		background-color: var(--cl5);
		color: var(--ac6_);
	}
	.good {
		background-color: var(--cl5);
	}
	.caution {
		background-color: var(--cl6);
	}
	.error {
		background-color: var(--cl4);
	}

	.date {
		font-size: smaller;
		color: var(--ac3);
	}
</style>

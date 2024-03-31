<script>
	export let voucher;
</script>

<a href="/admin/vouchers/{voucher.key}">
	<span class="date">
		{voucher.date}
	</span>
	<br />
	<div class="name">
		{voucher.key}
	</div>
	{voucher.value}
	|
	{voucher.status}
</a>

<style>
	a {
		display: block;
		padding: var(--sp2) 0;
		border-bottom: 2px solid var(--ac5);

		text-decoration: none;
		color: var(--ac2);
	}

	.name {
		color: var(--ac1);
		font-weight: 700;
	}

	.date {
		font-size: smaller;
		color: var(--ac3);
	}
</style>

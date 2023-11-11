<script>
	export let voucher;
</script>

<a href="/admin/vouchers/{voucher.key}">
	{voucher.date}
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
		font-weight: 500;
	}
</style>

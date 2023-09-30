<script>
	import Button from '$lib/button.svelte';
	export let voucher;
</script>

{voucher.date}
<br />
<Button class="link" href="/admin/vouchers/{voucher.key}">
	{voucher.key}
</Button>
<br />
{voucher.value}
|
{voucher.status}
<br />

<br />

<style>
</style>

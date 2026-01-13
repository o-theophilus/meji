<script>
	let { receiver } = $props();
</script>

<div class="receiver">
	<div>{receiver.name}</div>
	<div>{receiver.phone}</div>
	<div>{receiver.email}</div>

	<div>
		{receiver.address.address},
		{receiver.address.state},
		{receiver.address.country}
	</div>
</div>

<style>
	.receiver {
		font-size: 0.8rem;
	}
</style>

<script>
	import { Datetime } from '$lib/macro';

	let { datetime } = $props();

	const today = new Date();
	const nextWeek = new Date(today);
	nextWeek.setDate(today.getDate() + 7);
</script>

<hr style="border-color: gray; margin: 24px 0;" />
<b style="font-size: 0.8rem;">Delivery Date:</b>
<br />
<br />

Date:
<Datetime datetime={nextWeek} type="day_full" />,
<Datetime datetime={nextWeek} type="date_numeric" /><br />
Time:
<Datetime datetime={nextWeek} type="time_period" />

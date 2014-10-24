# -*- coding: utf-8 -*-

from django.db import models


class Accounts(models.Model):
    name = models.CharField(max_length=255)
    current_amount = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = u'Счет'
        verbose_name_plural = u'Счета'

    def __unicode__(self):
        return u'%s %s' % (self.name, self.current_amount)


class RegularMonthlyExpenses(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    account = models.ForeignKey(Accounts, null=True)

    class Meta:
        verbose_name = u'Постоянный месячный расход'
        verbose_name_plural = u'Постоянные месячные расходы'

    def __unicode__(self):
        return u'%s %s' % (self.name, self.amount)


class Envelopes(models.Model):
    name = models.CharField(max_length=255)
    current_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    monthly_replenishment = models.DecimalField(max_digits=8, decimal_places=2)
    cash = models.BooleanField(blank=True)
    account = models.ForeignKey(Accounts)

    class Meta:
        verbose_name = u"конверт"
        verbose_name_plural = u'Конверты'

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.monthly_replenishment, self.current_amount)

    def save(self, *args, **kwargs):
        if self.current_amount is None:
            self.current_amount = self.monthly_replenishment
            super(Envelopes, self).save(*args, **kwargs)
        else:
            new_amount = self.current_amount + self.monthly_replenishment
            self.current_amount = new_amount
            super(Envelopes, self).save(*args, **kwargs)


class Expenses(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    envelope = models.ForeignKey(Envelopes)

    class Meta:
        verbose_name = u'Расход'
        verbose_name_plural = u'Расходы'

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.amount, self.envelope)


class Incomes(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    account = models.ForeignKey(Accounts, null=True)

    class Meta:
        verbose_name = u'Доход'
        verbose_name_plural = u'Доходы'

    def __unicode__(self):
        return u'%s %s' % (self.name, self.amount)


